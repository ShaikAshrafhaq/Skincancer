from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with additional fields for skin cancer detection app."""
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class UserProfile(models.Model):
    """Extended user profile for medical information."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    medical_history = models.TextField(blank=True, null=True)
    skin_type = models.CharField(
        max_length=20,
        choices=[
            ('type1', 'Type I - Very Fair'),
            ('type2', 'Type II - Fair'),
            ('type3', 'Type III - Medium'),
            ('type4', 'Type IV - Olive'),
            ('type5', 'Type V - Brown'),
            ('type6', 'Type VI - Dark'),
        ],
        blank=True,
        null=True
    )
    family_history = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    emergency_phone = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"Profile for {self.user.email}"


class OTPVerification(models.Model):
    """Model to store OTP verification codes."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'otp_verifications'
    
    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp_code}"
