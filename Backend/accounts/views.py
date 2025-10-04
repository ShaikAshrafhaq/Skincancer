from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from datetime import datetime, timedelta
import random
import string

from .models import User, UserProfile, OTPVerification
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    OTPVerificationSerializer,
    UserSerializer,
    OTPSendSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """View for user registration."""
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate OTP for email verification
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # In a real application, you would send this OTP via email/SMS
        # For demo purposes, we'll return it in the response
        return Response({
            'message': 'User registered successfully. Please verify your email with the OTP.',
            'otp_code': otp_code,  # Remove this in production
            'requires_verification': True
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """View for user login."""
    
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate OTP for 2FA
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # In a real application, you would send this OTP via email/SMS
        # For demo purposes, we'll return it in the response
        return Response({
            'message': 'Please verify with OTP to complete login.',
            'otp_code': otp_code,  # Remove this in production
            'requires_2fa': True
        }, status=status.HTTP_200_OK)


class OTPVerificationView(generics.GenericAPIView):
    """View for OTP verification."""
    
    serializer_class = OTPVerificationSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        otp_verification = serializer.validated_data['otp_verification']
        
        # Mark OTP as used
        otp_verification.is_used = True
        otp_verification.save()
        
        # Mark user as verified
        user.is_verified = True
        user.save()
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        # Login user
        login(request, user)
        
        return Response({
            'message': 'OTP verified successfully.',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class ResendOTPView(generics.GenericAPIView):
    """View for resending OTP."""
    
    serializer_class = OTPSendSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate new OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # In a real application, you would send this OTP via email/SMS
        # For demo purposes, we'll return it in the response
        return Response({
            'message': 'New OTP sent successfully.',
            'otp_code': otp_code,  # Remove this in production
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for user profile."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """View for user logout."""
    try:
        # Delete the token
        request.user.auth_token.delete()
    except:
        pass
    
    logout(request)
    
    return Response({
        'message': 'Logged out successfully.'
    }, status=status.HTTP_200_OK)
