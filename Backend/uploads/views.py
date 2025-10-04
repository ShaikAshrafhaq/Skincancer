from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from PIL import Image
import os
import random

from .models import ImageUpload, AnalysisHistory
from .serializers import (
    ImageUploadSerializer, 
    ImageUploadCreateSerializer, 
    ImageUploadListSerializer,
    AnalysisHistorySerializer
)
from .analysis_service import SkinCancerAnalysisService


class ImageUploadCreateView(generics.CreateAPIView):
    """View for creating image uploads and running analysis."""
    
    serializer_class = ImageUploadCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        image_file = serializer.validated_data['image']
        
        # Process image
        try:
            with Image.open(image_file) as img:
                width, height = img.size
                file_size = image_file.size
                filename = image_file.name
        except Exception as e:
            return Response({
                'error': 'Invalid image file.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Run analysis
        analysis_service = SkinCancerAnalysisService()
        analysis_result = analysis_service.analyze_image(image_file, filename, width, height, file_size)
        
        # Create upload record
        upload = ImageUpload.objects.create(
            user=request.user,
            image=image_file,
            filename=filename,
            file_size=file_size,
            image_width=width,
            image_height=height,
            result=analysis_result['result'],
            confidence=analysis_result['confidence'],
            risk_score=analysis_result['risk_score'],
            cancer_type=analysis_result.get('cancer_type'),
            cancer_type_confidence=analysis_result.get('cancer_type_confidence', 0.0),
            cancer_type_name=analysis_result.get('cancer_type_name'),
            risk_level=analysis_result.get('risk_level', 'none'),
            should_consult_doctor=analysis_result['should_consult_doctor'],
            urgency_level=analysis_result['urgency_level'],
            recommendation_message=analysis_result['recommendation_message'],
            analysis_factors=analysis_result['analysis_factors']
        )
        
        # Return full upload data
        response_serializer = ImageUploadSerializer(upload)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ImageUploadListView(generics.ListAPIView):
    """View for listing user's image uploads with search and filtering."""
    
    serializer_class = ImageUploadListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['result', 'urgency_level', 'should_consult_doctor', 'cancer_type', 'risk_level']
    search_fields = ['filename', 'result', 'cancer_type_name']
    ordering_fields = ['created_at', 'confidence', 'risk_score', 'cancer_type_confidence']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get queryset filtered by user and search parameters."""
        queryset = ImageUpload.objects.filter(user=self.request.user)
        
        # Get search parameters
        search_query = self.request.query_params.get('search', None)
        filter_type = self.request.query_params.get('filter_type', None)
        
        # Apply search filter
        if search_query:
            queryset = queryset.filter(
                Q(filename__icontains=search_query) |
                Q(result__icontains=search_query) |
                Q(cancer_type_name__icontains=search_query)
            )
        
        # Apply result type filter
        if filter_type and filter_type != 'all':
            if filter_type == 'high-risk':
                queryset = queryset.filter(
                    Q(result='malignant') | Q(result='suspicious')
                )
            else:
                queryset = queryset.filter(result=filter_type)
        
        # Log search history
        if search_query or filter_type:
            AnalysisHistory.objects.create(
                user=self.request.user,
                search_query=search_query,
                filter_type=filter_type,
                results_count=queryset.count()
            )
        
        return queryset


class ImageUploadDetailView(generics.RetrieveDestroyAPIView):
    """View for retrieving and deleting individual image uploads."""
    
    serializer_class = ImageUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ImageUpload.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upload_statistics(request):
    """Get upload statistics for the user."""
    
    user_uploads = ImageUpload.objects.filter(user=request.user)
    
    total_uploads = user_uploads.count()
    benign_count = user_uploads.filter(result='benign').count()
    suspicious_count = user_uploads.filter(result='suspicious').count()
    malignant_count = user_uploads.filter(result='malignant').count()
    
    avg_confidence = user_uploads.aggregate(
        avg_confidence=models.Avg('confidence')
    )['avg_confidence'] or 0
    
    recent_uploads = user_uploads.filter(
        created_at__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()
    
    return Response({
        'total_uploads': total_uploads,
        'benign_count': benign_count,
        'suspicious_count': suspicious_count,
        'malignant_count': malignant_count,
        'average_confidence': round(avg_confidence, 1),
        'recent_uploads': recent_uploads,
        'high_risk_uploads': suspicious_count + malignant_count
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_upload_history(request):
    """Clear all upload history for the user."""
    
    if request.method == 'DELETE':
        deleted_count = ImageUpload.objects.filter(user=request.user).count()
        ImageUpload.objects.filter(user=request.user).delete()
        
        return Response({
            'message': f'Successfully deleted {deleted_count} uploads.',
            'deleted_count': deleted_count
        })
    
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
