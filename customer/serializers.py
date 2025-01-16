from rest_framework import serializers
from .import models
from django.contrib.auth.models import User
class CustomerSerializers(serializers.ModelSerializer):
    user=serializers.StringRelatedField(many=False)
    class Meta:
        model=models.Customer
        fields='__all__'
        
        
from rest_framework import serializers
from django.contrib.auth.models import User

class RegistratioSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def save(self, **kwargs):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Passwords don't match."})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists."})
        account = User(username=username, email=email)
        account.set_password(password)
        account.is_active=False
        account.save()
        return account


