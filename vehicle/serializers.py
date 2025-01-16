from rest_framework import serializers
from . import models

class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RiderRequest
        fields = '__all__'
        
        extra_kwargs = {
            'rent': {'required': False}  
        }

    def create(self, validated_data):
        rent = validated_data.pop('rent', None)
        instance = super().create(validated_data)
        if rent is not None:
            instance.rent = rent
            instance.save()
        return instance

class RentCalculationSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    destination = serializers.CharField(max_length=255)
    totalRent = serializers.FloatField(read_only=True)  
