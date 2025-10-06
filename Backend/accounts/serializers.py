from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, OTPVerification
import random
import string
from datetime import datetime, timedelta


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        
        # If no username provided, use email as username
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email']
        
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password.')
        
        return attrs


class OTPVerificationSerializer(serializers.Serializer):
    """Serializer for OTP verification."""
    
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')
        
        try:
            user = User.objects.get(email=email)
            otp_verification = OTPVerification.objects.filter(
                user=user,
                otp_code=otp_code,
                is_used=False,
                expires_at__gt=datetime.now()
            ).first()
            
            if not otp_verification:
                raise serializers.ValidationError('Invalid or expired OTP code.')
            
            attrs['user'] = user
            attrs['otp_verification'] = otp_verification
            
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data."""
    
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_verified', 'created_at', 'profile')
        read_only_fields = ('id', 'email', 'created_at', 'is_verified')


class OTPSendSerializer(serializers.Serializer):
    """Serializer for sending OTP."""
    
    email = serializers.EmailField()
    
    def generate_otp(self):
        """Generate a 6-digit OTP code."""
        return ''.join(random.choices(string.digits, k=6))
    
    def validate(self, attrs):
        email = attrs.get('email')
        
        try:
            user = User.objects.get(email=email)
            attrs['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        
        return attrs
