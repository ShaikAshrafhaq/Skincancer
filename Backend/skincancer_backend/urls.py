"""
URL configuration for skincancer_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root(request):
    """Root API endpoint providing information about available endpoints."""
    return JsonResponse({
        'message': 'Skin Cancer Detection API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'authentication': '/api/auth/',
            'uploads': '/api/uploads/',
            'analysis': '/api/analysis/',
        },
        'documentation': {
            'authentication': {
                'register': 'POST /api/auth/register/',
                'login': 'POST /api/auth/login/',
                'verify_otp': 'POST /api/auth/verify-otp/',
                'resend_otp': 'POST /api/auth/resend-otp/',
                'profile': 'GET /api/auth/profile/',
                'logout': 'POST /api/auth/logout/',
            },
            'uploads': {
                'upload_image': 'POST /api/uploads/',
                'list_uploads': 'GET /api/uploads/',
                'upload_detail': 'GET /api/uploads/{id}/',
                'delete_upload': 'DELETE /api/uploads/{id}/',
                'statistics': 'GET /api/uploads/statistics/',
                'clear_history': 'DELETE /api/uploads/clear-history/',
            },
            'analysis': {
                'dashboard_stats': 'GET /api/analysis/dashboard/',
                'trends': 'GET /api/analysis/trends/',
                'risk_assessment': 'GET /api/analysis/risk-assessment/',
            }
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/uploads/', include('uploads.urls')),
    path('api/analysis/', include('analysis.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
