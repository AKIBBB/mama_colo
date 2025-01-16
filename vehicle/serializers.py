from rest_framework import serializers
from .import models

class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.RiderRequest
        fields='__all__'
        
    
    
class RentCalculationSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    destination = serializers.CharField(max_length=255)
    totalRent = serializers.FloatField()