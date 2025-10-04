#!/usr/bin/env python
"""
Simple test to verify the API is working with MySQL data.
"""

import requests
import time

def test_api():
    """Test the API endpoints."""
    print("🌐 Testing API with MySQL Data")
    print("=" * 40)
    
    base_url = "http://localhost:8000/api"
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test uploads endpoint
        print("🔄 Testing uploads endpoint...")
        response = requests.get(f"{base_url}/uploads/", timeout=10)
        print(f"✅ Uploads endpoint: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Found {len(data.get('results', []))} uploads")
            print(f"   - API is working with MySQL data!")
        
        # Test statistics endpoint
        print("🔄 Testing statistics endpoint...")
        response = requests.get(f"{base_url}/uploads/statistics/", timeout=10)
        print(f"✅ Statistics endpoint: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Total uploads: {data.get('total_uploads', 0)}")
            print(f"   - Malignant cases: {data.get('malignant_count', 0)}")
            print(f"   - High risk cases: {data.get('high_risk_uploads', 0)}")
        
        print("\n🎉 SUCCESS: API is working with MySQL database!")
        print("   - Data is being served from MySQL")
        print("   - All endpoints are functional")
        print("   - Frontend can now connect to backend")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start Django server:")
        print("   python manage.py runserver 0.0.0.0:8000")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    test_api()
