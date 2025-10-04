#!/usr/bin/env python3
"""
Database setup script for Skin Cancer Detection Backend
This script creates the MySQL database and runs migrations
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

def create_database():
    """Create the MySQL database if it doesn't exist"""
    try:
        # Connect to MySQL server without specifying database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ashraf@12',
            port=3306
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS skincancer_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'skincancer_db' created successfully or already exists")
            
            # Show databases to confirm
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("📋 Available databases:")
            for db in databases:
                print(f"   - {db[0]}")
                
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 MySQL connection closed")
    
    return True

def run_migrations():
    """Run Django migrations"""
    try:
        from django.core.management import execute_from_command_line
        print("\n🔄 Running Django migrations...")
        
        # Make migrations
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✅ Made migrations")
        
        # Apply migrations
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Applied migrations")
        
        return True
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

def create_superuser():
    """Create a Django superuser"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superuser already exists")
            return True
            
        # Create superuser
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@skincancer.com',
            password='admin123'
        )
        print("✅ Superuser created successfully")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@skincancer.com")
        
        return True
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Skin Cancer Detection Backend Database")
    print("=" * 50)
    
    # Step 1: Create database
    print("\n1️⃣ Creating MySQL database...")
    if not create_database():
        print("❌ Failed to create database. Please check your MySQL connection.")
        return False
    
    # Step 2: Run migrations
    print("\n2️⃣ Running Django migrations...")
    if not run_migrations():
        print("❌ Failed to run migrations.")
        return False
    
    # Step 3: Create superuser
    print("\n3️⃣ Creating superuser...")
    if not create_superuser():
        print("❌ Failed to create superuser.")
        return False
    
    print("\n🎉 Database setup completed successfully!")
    print("\n📝 Next steps:")
    print("   1. Start the Django server: python manage.py runserver")
    print("   2. Access admin panel: http://localhost:8000/admin/")
    print("   3. Login with: admin / admin123")
    
    return True

if __name__ == "__main__":
    main()
