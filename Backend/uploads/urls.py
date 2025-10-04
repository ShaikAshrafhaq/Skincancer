from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImageUploadCreateView.as_view(), name='upload-create'),
    path('list/', views.ImageUploadListView.as_view(), name='upload-list'),
    path('<uuid:pk>/', views.ImageUploadDetailView.as_view(), name='upload-detail'),
    path('statistics/', views.upload_statistics, name='upload-statistics'),
    path('clear-history/', views.clear_upload_history, name='clear-history'),
]
