#!/usr/bin/env python3
"""
Test MySQL database connection for Skin Cancer Detection Backend
"""

import mysql.connector
from mysql.connector import Error
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincancer_backend.settings')
django.setup()

def test_mysql_connection():
    """Test direct MySQL connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ashraf@12',
            port=3306,
            database='skincancer_db'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL connection successful!")
            print(f"   MySQL version: {version[0]}")
            
            # Test database operations
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"   Tables in database: {len(tables)}")
            for table in tables:
                print(f"     - {table[0]}")
            
            return True
            
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 MySQL connection closed")

def test_django_connection():
    """Test Django database connection"""
    try:
        from django.db import connection
        from django.core.management import execute_from_command_line
        
        # Test Django database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Django database connection successful!")
            print(f"   Test query result: {result[0]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Django database connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Database Connections")
    print("=" * 40)
    
    # Test 1: Direct MySQL connection
    print("\n1️⃣ Testing direct MySQL connection...")
    mysql_success = test_mysql_connection()
    
    # Test 2: Django database connection
    print("\n2️⃣ Testing Django database connection...")
    django_success = test_django_connection()
    
    # Summary
    print("\n📊 Test Results:")
    print(f"   MySQL Connection: {'✅ PASS' if mysql_success else '❌ FAIL'}")
    print(f"   Django Connection: {'✅ PASS' if django_success else '❌ FAIL'}")
    
    if mysql_success and django_success:
        print("\n🎉 All database connections are working correctly!")
        return True
    else:
        print("\n❌ Some database connections failed. Please check your configuration.")
        return False

if __name__ == "__main__":
    main()
