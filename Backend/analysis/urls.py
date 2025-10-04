from django.urls import path
from . import views

urlpatterns = [
    path('dashboard-stats/', views.dashboard_statistics, name='dashboard-statistics'),
    path('trends/', views.analysis_trends, name='analysis-trends'),
    path('risk-assessment/', views.risk_assessment, name='risk-assessment'),
]
