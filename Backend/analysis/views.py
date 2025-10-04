from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta

from uploads.models import ImageUpload


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_statistics(request):
    """Get comprehensive dashboard statistics for the user."""
    
    user = request.user
    user_uploads = ImageUpload.objects.filter(user=user)
    
    # Basic statistics
    total_uploads = user_uploads.count()
    
    # Result breakdown
    result_stats = user_uploads.values('result').annotate(count=Count('id'))
    benign_count = next((item['count'] for item in result_stats if item['result'] == 'benign'), 0)
    suspicious_count = next((item['count'] for item in result_stats if item['result'] == 'suspicious'), 0)
    malignant_count = next((item['count'] for item in result_stats if item['result'] == 'malignant'), 0)
    
    # Confidence statistics
    avg_confidence = user_uploads.aggregate(avg_confidence=Avg('confidence'))['avg_confidence'] or 0
    
    # Time-based statistics
    now = timezone.now()
    last_7_days = user_uploads.filter(created_at__gte=now - timedelta(days=7)).count()
    last_30_days = user_uploads.filter(created_at__gte=now - timedelta(days=30)).count()
    
    # Risk statistics
    high_risk_uploads = suspicious_count + malignant_count
    risk_percentage = (high_risk_uploads / total_uploads * 100) if total_uploads > 0 else 0
    
    # Recent uploads (last 5)
    recent_uploads = user_uploads.order_by('-created_at')[:5]
    recent_uploads_data = []
    for upload in recent_uploads:
        recent_uploads_data.append({
            'id': str(upload.id),
            'filename': upload.filename,
            'result': upload.result,
            'confidence': upload.confidence,
            'created_at': upload.created_at,
            'should_consult_doctor': upload.should_consult_doctor,
            'urgency_level': upload.urgency_level
        })
    
    return Response({
        'total_uploads': total_uploads,
        'result_breakdown': {
            'benign': benign_count,
            'suspicious': suspicious_count,
            'malignant': malignant_count
        },
        'average_confidence': round(avg_confidence, 1),
        'high_risk_uploads': high_risk_uploads,
        'risk_percentage': round(risk_percentage, 1),
        'recent_activity': {
            'last_7_days': last_7_days,
            'last_30_days': last_30_days
        },
        'recent_uploads': recent_uploads_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analysis_trends(request):
    """Get analysis trends over time."""
    
    user = request.user
    user_uploads = ImageUpload.objects.filter(user=user)
    
    # Get uploads from last 30 days
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    recent_uploads = user_uploads.filter(created_at__gte=thirty_days_ago)
    
    # Group by day
    daily_stats = {}
    for i in range(30):
        date = (now - timedelta(days=i)).date()
        day_uploads = recent_uploads.filter(created_at__date=date)
        
        daily_stats[date.isoformat()] = {
            'total': day_uploads.count(),
            'benign': day_uploads.filter(result='benign').count(),
            'suspicious': day_uploads.filter(result='suspicious').count(),
            'malignant': day_uploads.filter(result='malignant').count(),
            'avg_confidence': round(day_uploads.aggregate(avg=Avg('confidence'))['avg'] or 0, 1)
        }
    
    return Response({
        'daily_trends': daily_stats,
        'period': '30_days'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def risk_assessment(request):
    """Get comprehensive risk assessment for the user."""
    
    user = request.user
    user_uploads = ImageUpload.objects.filter(user=user)
    
    if not user_uploads.exists():
        return Response({
            'risk_level': 'unknown',
            'message': 'No uploads available for risk assessment.',
            'recommendations': [
                'Upload skin lesion images to get personalized risk assessment.',
                'Regular skin self-examinations are recommended.',
                'Consult a dermatologist for professional skin cancer screening.'
            ]
        })
    
    # Calculate risk metrics
    total_uploads = user_uploads.count()
    high_risk_uploads = user_uploads.filter(
        result__in=['suspicious', 'malignant']
    ).count()
    
    recent_high_risk = user_uploads.filter(
        result__in=['suspicious', 'malignant'],
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    avg_confidence = user_uploads.aggregate(avg=Avg('confidence'))['avg'] or 0
    
    # Determine overall risk level
    if high_risk_uploads == 0:
        risk_level = 'low'
        message = 'Your skin analysis shows no concerning results.'
    elif high_risk_uploads <= total_uploads * 0.1:  # Less than 10% high risk
        risk_level = 'low'
        message = 'Your skin analysis shows mostly benign results with minimal concerns.'
    elif high_risk_uploads <= total_uploads * 0.3:  # 10-30% high risk
        risk_level = 'medium'
        message = 'Your skin analysis shows some concerning results that warrant attention.'
    else:  # More than 30% high risk
        risk_level = 'high'
        message = 'Your skin analysis shows multiple concerning results requiring immediate attention.'
    
    # Generate recommendations
    recommendations = []
    
    if risk_level == 'high':
        recommendations.extend([
            'Schedule an immediate appointment with a dermatologist.',
            'Consider more frequent skin self-examinations.',
            'Discuss family history of skin cancer with your healthcare provider.',
            'Ensure proper sun protection measures are in place.'
        ])
    elif risk_level == 'medium':
        recommendations.extend([
            'Schedule a dermatologist appointment within 2-4 weeks.',
            'Increase frequency of skin self-examinations.',
            'Review sun protection habits and improve if needed.',
            'Consider annual professional skin cancer screening.'
        ])
    else:
        recommendations.extend([
            'Continue regular skin self-examinations.',
            'Maintain good sun protection habits.',
            'Consider annual professional skin cancer screening.',
            'Stay vigilant for any new or changing skin lesions.'
        ])
    
    return Response({
        'risk_level': risk_level,
        'message': message,
        'metrics': {
            'total_uploads': total_uploads,
            'high_risk_uploads': high_risk_uploads,
            'recent_high_risk': recent_high_risk,
            'average_confidence': round(avg_confidence, 1),
            'risk_percentage': round((high_risk_uploads / total_uploads) * 100, 1)
        },
        'recommendations': recommendations
    })
