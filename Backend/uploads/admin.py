from django.contrib import admin
from .models import ImageUpload, AnalysisHistory


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    """Admin for ImageUpload model."""
    
    list_display = ('user', 'filename', 'result', 'confidence', 'urgency_level', 'created_at')
    list_filter = ('result', 'urgency_level', 'should_consult_doctor', 'created_at')
    search_fields = ('user__email', 'filename', 'result')
    readonly_fields = ('id', 'created_at', 'updated_at', 'image_url', 'confidence_percentage')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'image', 'image_url', 'filename', 'file_size')
        }),
        ('Image Details', {
            'fields': ('image_width', 'image_height', 'created_at', 'updated_at')
        }),
        ('Analysis Results', {
            'fields': ('result', 'confidence', 'confidence_percentage', 'risk_score')
        }),
        ('Medical Recommendations', {
            'fields': ('should_consult_doctor', 'urgency_level', 'recommendation_message')
        }),
        ('Analysis Factors', {
            'fields': ('analysis_factors',),
            'classes': ('collapse',)
        }),
    )


@admin.register(AnalysisHistory)
class AnalysisHistoryAdmin(admin.ModelAdmin):
    """Admin for AnalysisHistory model."""
    
    list_display = ('user', 'search_query', 'filter_type', 'results_count', 'created_at')
    list_filter = ('filter_type', 'created_at')
    search_fields = ('user__email', 'search_query')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
