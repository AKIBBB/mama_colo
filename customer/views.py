from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import viewsets
from .import models
from .import serializers
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils.encoding import force_str
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
# Create your views here.
class CustomerViewset(viewsets.ModelViewSet):
    queryset=models.Customer.objects.all()
    serializer_class=serializers.CustomerSerializers
    
    
class UserReApiViewgistration(APIView):
    serializer_class = serializers.RegistratioSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/customer/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('auth_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response({"message": "Check your mail for confirmation"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')  
    else:
        return redirect('register')  

    
    
    
class UserLoginApiView(APIView):
    def post(self,request):
        serializer= serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password']
            
            user=authenticate(username=username,password=password)
            
            if user:
                token, _=Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token' :token.key, 'user_id' :user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)
    
    
    


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        if not request.auth:
            raise AuthenticationFailed("Authentication token not provided or invalid.")
        request.auth.delete()
        return Response({"message": "Logged out successfully"}, status=200)
    
    
class CustomerProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Retrieve the profile of the authenticated user
            customer = User.Customer.objects.get(user=request.user)
            serializer =serializers.CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.Customer.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            # Update the profile of the authenticated user
            customer =User.Customer.objects.get(user=request.user)
            serializer = serializers.CustomerSerializers(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.Customer.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)