from django.shortcuts import render
from rest_framework import viewsets
from .import models
from .import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RiderRequest
from .serializers import RideRequestSerializer
from driver.models import Driver
import requests

# Create your views here.
class RideRequestViewset(viewsets.ModelViewSet):
    queryset=models.RiderRequest.objects.all()
    serializer_class=serializers.RideRequestSerializer
    
    
class RideRequestListCreateAPIView(APIView):
    def get(self, request):
        # List all ride requests
        ride_requests = RiderRequest.objects.filter(cancel=False)
        serializer = RideRequestSerializer(ride_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Extract address and destination from the request
        address = request.data.get('address')
        destination = request.data.get('destination')

        # Replace with your Mapbox access token
        MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiYWtpYmJiIiwiYSI6ImNtNXl4NHhsMTA0M3gyaXNha29pdWxqcjEifQ.ObzNOr6k1cbDDcrPbdzOWA'
        
        # API request to Mapbox for directions
        response = requests.get(f'https://api.mapbox.com/directions/v5/mapbox/driving/{address};{destination}?access_token={MAPBOX_ACCESS_TOKEN}')
        
        if response.status_code == 200:
            # Calculate rent based on distance
            data = response.json()
            distance_in_m = data['routes'][0]['distance']
            distance_in_km = distance_in_m / 1000  
            cost_per_km = 3  # Adjust cost per km as needed
            total_rent = distance_in_km * cost_per_km

            # Save the ride request with the calculated rent
            ride_data = request.data.copy()  # Make a mutable copy of the request data
            ride_data['rent'] = total_rent  # Add the calculated rent to the data
            
            serializer = RideRequestSerializer(data=ride_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Could not calculate distance'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AcceptRideRequestAPIView(APIView):
    def post(self, request, pk):
        try:
            ride_request = RiderRequest.objects.get(pk=pk, cancel=False)
        except RiderRequest.DoesNotExist:
            return Response({'error': 'Ride request not found or cancelled'}, status=status.HTTP_404_NOT_FOUND)

        driver_id = request.data.get('driver_id')
        try:
            driver = Driver.objects.get(id=driver_id)
        except Driver.DoesNotExist:
            return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)

        if ride_request.driver:
            return Response({'error': 'Ride request already accepted'}, status=status.HTTP_400_BAD_REQUEST)

        ride_request.driver = driver
        ride_request.status = 'Running'
        ride_request.save()

        return Response({'message': 'Ride request accepted successfully'}, status=status.HTTP_200_OK)