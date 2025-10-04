from django.db import models
from django.conf import settings
import uuid
import os


def upload_to(instance, filename):
    """Generate upload path for images."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', 'images', filename)


class ImageUpload(models.Model):
    """Model for storing uploaded images and analysis results."""
    
    RESULT_CHOICES = [
        ('benign', 'Benign'),
        ('malignant', 'Malignant'),
        ('suspicious', 'Suspicious'),
    ]
    
    CANCER_TYPE_CHOICES = [
        ('melanoma', 'Melanoma'),
        ('basal_cell_carcinoma', 'Basal Cell Carcinoma'),
        ('squamous_cell_carcinoma', 'Squamous Cell Carcinoma'),
        ('merkel_cell_carcinoma', 'Merkel Cell Carcinoma'),
        ('sebaceous_gland_carcinoma', 'Sebaceous Gland Carcinoma'),
        ('actinic_keratosis', 'Actinic Keratosis'),
        ('seborrheic_keratosis', 'Seborrheic Keratosis'),
        ('benign_mole', 'Benign Mole'),
    ]
    
    URGENCY_CHOICES = [
        ('none', 'None'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('immediate', 'Immediate'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('none', 'None'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploads')
    image = models.ImageField(upload_to=upload_to)
    filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    
    # Analysis results
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    confidence = models.FloatField()
    risk_score = models.FloatField()
    
    # Cancer type detection
    cancer_type = models.CharField(max_length=30, choices=CANCER_TYPE_CHOICES, blank=True, null=True)
    cancer_type_confidence = models.FloatField(default=0.0)
    cancer_type_name = models.CharField(max_length=100, blank=True, null=True)
    risk_level = models.CharField(max_length=15, choices=RISK_LEVEL_CHOICES, default='none')
    
    # Medical recommendations
    should_consult_doctor = models.BooleanField(default=False)
    urgency_level = models.CharField(max_length=15, choices=URGENCY_CHOICES, default='none')
    recommendation_message = models.TextField()
    
    # Metadata
    analysis_factors = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'image_uploads'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.filename} ({self.result})"
    
    @property
    def image_url(self):
        """Return the URL of the uploaded image."""
        if self.image:
            return self.image.url
        return None
    
    @property
    def confidence_percentage(self):
        """Return confidence as percentage."""
        return f"{self.confidence:.1f}%"
    
    def get_doctor_recommendation(self):
        """Get doctor recommendation based on result and confidence."""
        if self.result == 'malignant':
            return {
                'should_consult': True,
                'urgency': 'high',
                'message': '⚠️ URGENT: Consult a dermatologist immediately',
                'color': '#F44336'
            }
        elif self.result == 'suspicious':
            return {
                'should_consult': True,
                'urgency': 'medium',
                'message': '🔍 RECOMMENDED: Schedule a dermatologist appointment within 1-2 weeks',
                'color': '#FF9800'
            }
        elif self.result == 'benign' and self.confidence < 80:
            return {
                'should_consult': True,
                'urgency': 'low',
                'message': '💡 SUGGESTED: Consider a routine check-up for peace of mind',
                'color': '#2196F3'
            }
        else:
            return {
                'should_consult': False,
                'urgency': 'none',
                'message': '✅ No immediate concern, but regular skin checks are always recommended',
                'color': '#4CAF50'
            }


class AnalysisHistory(models.Model):
    """Model for storing analysis history and search queries."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analysis_history')
    search_query = models.CharField(max_length=255, blank=True, null=True)
    filter_type = models.CharField(max_length=20, blank=True, null=True)
    results_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analysis_history'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.search_query or 'No search'} ({self.results_count} results)"
