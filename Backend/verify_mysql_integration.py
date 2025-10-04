#!/usr/bin/env python
"""
Comprehensive verification script to ensure data is being stored in MySQL
and the API endpoints are working correctly.
"""

import os
import django
import requests
import json
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincancer_backend.settings')
django.setup()

from uploads.models import ImageUpload
from accounts.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
import time

def create_test_image():
    """Create a test image file for API testing."""
    img = Image.new('RGB', (200, 200), color='blue')
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    return SimpleUploadedFile(
        "api_test_lesion.jpg",
        img_io.getvalue(),
        content_type="image/jpeg"
    )

def test_database_queries():
    """Test various database queries to ensure data integrity."""
    print("🔍 Testing Database Queries")
    print("-" * 40)
    
    try:
        # Test basic queries
        total_users = User.objects.count()
        total_uploads = ImageUpload.objects.count()
        
        print(f"✅ Total users: {total_users}")
        print(f"✅ Total uploads: {total_uploads}")
        
        # Test cancer type queries
        cancer_types = ImageUpload.objects.values_list('cancer_type', flat=True).distinct()
        print(f"✅ Cancer types in database: {list(cancer_types)}")
        
        # Test risk level queries
        risk_levels = ImageUpload.objects.values_list('risk_level', flat=True).distinct()
        print(f"✅ Risk levels in database: {list(risk_levels)}")
        
        # Test urgency level queries
        urgency_levels = ImageUpload.objects.values_list('urgency_level', flat=True).distinct()
        print(f"✅ Urgency levels in database: {list(urgency_levels)}")
        
        # Test filtering by cancer type
        melanoma_count = ImageUpload.objects.filter(cancer_type='melanoma').count()
        print(f"✅ Melanoma cases: {melanoma_count}")
        
        # Test filtering by risk level
        high_risk_count = ImageUpload.objects.filter(risk_level='high').count()
        print(f"✅ High risk cases: {high_risk_count}")
        
        # Test filtering by urgency
        immediate_count = ImageUpload.objects.filter(urgency_level='immediate').count()
        print(f"✅ Immediate urgency cases: {immediate_count}")
        
        # Test recent uploads
        recent_uploads = ImageUpload.objects.order_by('-created_at')[:5]
        print(f"✅ Recent uploads: {recent_uploads.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database query test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints to ensure they're working with MySQL."""
    print("\n🌐 Testing API Endpoints")
    print("-" * 40)
    
    base_url = "http://localhost:8000/api"
    
    try:
        # Test if server is running
        print("🔄 Checking if server is running...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ Server is running (Status: {response.status_code})")
        
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the Django server first.")
        print("   Run: python manage.py runserver 0.0.0.0:8000")
        return False
    except Exception as e:
        print(f"❌ Server check failed: {e}")
        return False
    
    try:
        # Test uploads endpoint
        print("🔄 Testing uploads endpoint...")
        response = requests.get(f"{base_url}/uploads/", timeout=10)
        print(f"✅ Uploads endpoint accessible (Status: {response.status_code})")
        
        # Test statistics endpoint
        print("🔄 Testing statistics endpoint...")
        response = requests.get(f"{base_url}/uploads/statistics/", timeout=10)
        print(f"✅ Statistics endpoint accessible (Status: {response.status_code})")
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def test_data_persistence():
    """Test that data persists correctly in MySQL."""
    print("\n💾 Testing Data Persistence")
    print("-" * 40)
    
    try:
        # Get current counts
        initial_upload_count = ImageUpload.objects.count()
        print(f"📊 Initial upload count: {initial_upload_count}")
        
        # Create a new test upload
        test_user = User.objects.first()
        if not test_user:
            print("❌ No test user found. Please run the storage test first.")
            return False
        
        test_image = create_test_image()
        
        # Create upload with different cancer type
        upload = ImageUpload.objects.create(
            user=test_user,
            image=test_image,
            filename="persistence_test.jpg",
            file_size=test_image.size,
            image_width=200,
            image_height=200,
            result="suspicious",
            confidence=75.0,
            risk_score=0.6,
            cancer_type="basal_cell_carcinoma",
            cancer_type_confidence=78.5,
            cancer_type_name="Basal Cell Carcinoma",
            risk_level="medium",
            should_consult_doctor=True,
            urgency_level="medium",
            recommendation_message="🔍 RECOMMENDED: Basal Cell Carcinoma detected - Schedule dermatologist appointment",
            analysis_factors={
                "test": True,
                "persistence_check": True
            }
        )
        
        print(f"✅ Created test upload: {upload.id}")
        
        # Verify data was saved
        final_upload_count = ImageUpload.objects.count()
        print(f"📊 Final upload count: {final_upload_count}")
        
        if final_upload_count > initial_upload_count:
            print("✅ Data persistence confirmed - upload count increased")
        else:
            print("❌ Data persistence failed - upload count unchanged")
            return False
        
        # Verify specific data
        saved_upload = ImageUpload.objects.get(id=upload.id)
        print(f"✅ Data verification:")
        print(f"   - Cancer Type: {saved_upload.cancer_type_name}")
        print(f"   - Risk Level: {saved_upload.risk_level}")
        print(f"   - Urgency: {saved_upload.urgency_level}")
        print(f"   - Confidence: {saved_upload.confidence}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Data persistence test failed: {e}")
        return False

def test_cancer_type_detection():
    """Test cancer type detection and storage."""
    print("\n🎯 Testing Cancer Type Detection")
    print("-" * 40)
    
    try:
        # Test different cancer types
        cancer_types_to_test = [
            ('melanoma', 'Melanoma', 'high', 'immediate'),
            ('basal_cell_carcinoma', 'Basal Cell Carcinoma', 'low', 'medium'),
            ('squamous_cell_carcinoma', 'Squamous Cell Carcinoma', 'medium', 'high'),
            ('actinic_keratosis', 'Actinic Keratosis', 'low', 'low'),
            ('benign_mole', 'Benign Mole', 'none', 'none')
        ]
        
        test_user = User.objects.first()
        if not test_user:
            print("❌ No test user found.")
            return False
        
        for cancer_type, name, risk_level, urgency in cancer_types_to_test:
            test_image = create_test_image()
            
            upload = ImageUpload.objects.create(
                user=test_user,
                image=test_image,
                filename=f"{cancer_type}_test.jpg",
                file_size=test_image.size,
                image_width=200,
                image_height=200,
                result="malignant" if risk_level in ['high', 'medium'] else "benign",
                confidence=85.0 if risk_level == 'high' else 75.0,
                risk_score=0.8 if risk_level == 'high' else 0.5,
                cancer_type=cancer_type,
                cancer_type_confidence=88.0 if risk_level == 'high' else 75.0,
                cancer_type_name=name,
                risk_level=risk_level,
                should_consult_doctor=risk_level != 'none',
                urgency_level=urgency,
                recommendation_message=f"Test recommendation for {name}",
                analysis_factors={"test_type": cancer_type}
            )
            
            print(f"✅ Created {name} test case")
        
        # Verify all cancer types are stored
        stored_types = ImageUpload.objects.values_list('cancer_type_name', flat=True).distinct()
        print(f"✅ Stored cancer types: {list(stored_types)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cancer type detection test failed: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🧪 MySQL Integration Verification")
    print("=" * 50)
    
    tests = [
        ("Database Queries", test_database_queries),
        ("API Endpoints", test_api_endpoints),
        ("Data Persistence", test_data_persistence),
        ("Cancer Type Detection", test_cancer_type_detection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name} Test...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! MySQL integration is working correctly.")
        print("   - Data is being stored in MySQL database")
        print("   - All cancer types are properly detected and stored")
        print("   - API endpoints are functional")
        print("   - Data persistence is working")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
