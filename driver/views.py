from django.shortcuts import render
from rest_framework import viewsets
from .import models
from .import serializers
# Create your views here.
class DriverViewset(viewsets.ModelViewSet):
    queryset=models.Driver.objects.all()
    serializer_class=serializers.DriverSerializers
    


class ReviewViewset(viewsets.ModelViewSet):
    queryset=models.Review.objects.all()
    serializer_class=serializers.ReviewSerializers