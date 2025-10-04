from rest_framework import serializers
from .models import ImageUpload, AnalysisHistory
from accounts.serializers import UserSerializer


class ImageUploadSerializer(serializers.ModelSerializer):
    """Serializer for image uploads."""
    
    user = UserSerializer(read_only=True)
    image_url = serializers.ReadOnlyField()
    confidence_percentage = serializers.ReadOnlyField()
    doctor_recommendation = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageUpload
        fields = [
            'id', 'user', 'image', 'image_url', 'filename', 'file_size',
            'image_width', 'image_height', 'result', 'confidence', 'confidence_percentage',
            'risk_score', 'cancer_type', 'cancer_type_confidence', 'cancer_type_name', 'risk_level',
            'should_consult_doctor', 'urgency_level', 'recommendation_message',
            'analysis_factors', 'created_at', 'updated_at', 'doctor_recommendation'
        ]
        read_only_fields = [
            'id', 'user', 'image_url', 'confidence_percentage', 'doctor_recommendation',
            'created_at', 'updated_at'
        ]
    
    def get_doctor_recommendation(self, obj):
        """Get doctor recommendation for the upload."""
        return obj.get_doctor_recommendation()


class ImageUploadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating image uploads."""
    
    class Meta:
        model = ImageUpload
        fields = ['image']
    
    def validate_image(self, value):
        """Validate uploaded image."""
        # Check file size (10MB limit)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image file is too large. Maximum size is 10MB.")
        
        # Check file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Invalid file type. Please upload JPEG, PNG, BMP, or TIFF images.")
        
        return value


class AnalysisHistorySerializer(serializers.ModelSerializer):
    """Serializer for analysis history."""
    
    class Meta:
        model = AnalysisHistory
        fields = ['id', 'search_query', 'filter_type', 'results_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class ImageUploadListSerializer(serializers.ModelSerializer):
    """Simplified serializer for image upload lists."""
    
    image_url = serializers.ReadOnlyField()
    confidence_percentage = serializers.ReadOnlyField()
    doctor_recommendation = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageUpload
        fields = [
            'id', 'image_url', 'filename', 'result', 'confidence_percentage',
            'cancer_type', 'cancer_type_name', 'cancer_type_confidence', 'risk_level',
            'should_consult_doctor', 'urgency_level', 'created_at', 'doctor_recommendation'
        ]
    
    def get_doctor_recommendation(self, obj):
        """Get doctor recommendation for the upload."""
        return obj.get_doctor_recommendation()
