#!/usr/bin/env python
"""
Setup script for Skin Cancer Detection Backend
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def setup_django_backend():
    """Setup Django backend for Skin Cancer Detection."""
    
    print("🏥 Setting up Skin Cancer Detection Backend...")
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ manage.py not found. Please run this script from the Backend directory.")
        return False
    
    # Create necessary directories
    directories = ['logs', 'media/uploads/images', 'staticfiles']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Run Django migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Running database migrations"):
        return False
    
    # Create superuser (optional)
    print("\n👤 Would you like to create a superuser? (y/n): ", end="")
    create_superuser = input().lower().strip()
    if create_superuser == 'y':
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    print("\n🎉 Django backend setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy env_example.txt to .env and configure your settings")
    print("2. Run: python manage.py runserver")
    print("3. Access admin at: http://localhost:8000/admin/")
    print("4. API endpoints available at: http://localhost:8000/api/")
    
    return True

if __name__ == "__main__":
    setup_django_backend()
