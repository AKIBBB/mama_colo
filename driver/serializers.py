from rest_framework import serializers
from .import models
class DriverSerializers(serializers.ModelSerializer):
    user=serializers.StringRelatedField(many=False)
    class Meta:
        model=models.Driver
        fields='__all__'
        
        
        
class ReviewSerializers(serializers.ModelSerializer):
    user=serializers.StringRelatedField(many=False)
    class Meta:
        model=models.Review
        fields='__all__'