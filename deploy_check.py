#!/usr/bin/env python
"""
Deployment verification script for Render.com
Checks if all necessary files and configurations are in place.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status."""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_directory_structure():
    """Check if the project has the correct directory structure."""
    print("🔍 Checking project structure...")
    print("=" * 50)
    
    required_files = [
        ("render.yaml", "Render.com deployment configuration"),
        ("build.sh", "Build script"),
        ("README.md", "Project documentation"),
        ("Backend/requirements.txt", "Python dependencies"),
        ("Backend/manage.py", "Django management script"),
        ("Backend/skincancer_backend/settings.py", "Django settings"),
        ("Frontend/@/package.json", "Frontend dependencies"),
        ("Frontend/@/vite.config.js", "Vite configuration"),
    ]
    
    all_good = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    return all_good

def check_render_yaml():
    """Check if render.yaml has the correct configuration."""
    print("\n🔍 Checking render.yaml configuration...")
    print("=" * 50)
    
    try:
        with open("render.yaml", "r") as f:
            content = f.read()
        
        required_sections = [
            "services:",
            "skincancer-backend",
            "skincancer-frontend",
            "databases:",
            "skincancer-db"
        ]
        
        all_sections_found = True
        for section in required_sections:
            if section in content:
                print(f"✅ Found: {section}")
            else:
                print(f"❌ Missing: {section}")
                all_sections_found = False
        
        return all_sections_found
        
    except Exception as e:
        print(f"❌ Error reading render.yaml: {e}")
        return False

def check_backend_config():
    """Check if backend is properly configured for production."""
    print("\n🔍 Checking backend configuration...")
    print("=" * 50)
    
    try:
        # Check if settings.py has production configurations
        with open("Backend/skincancer_backend/settings.py", "r") as f:
            content = f.read()
        
        required_configs = [
            "dj_database_url",
            "DATABASE_URL",
            "ALLOWED_HOSTS",
            "CORS_ALLOWED_ORIGINS",
            "STATIC_ROOT",
            "MEDIA_ROOT"
        ]
        
        all_configs_found = True
        for config in required_configs:
            if config in content:
                print(f"✅ Found: {config}")
            else:
                print(f"❌ Missing: {config}")
                all_configs_found = False
        
        return all_configs_found
        
    except Exception as e:
        print(f"❌ Error checking backend config: {e}")
        return False

def check_frontend_config():
    """Check if frontend is properly configured."""
    print("\n🔍 Checking frontend configuration...")
    print("=" * 50)
    
    try:
        # Check package.json
        with open("Frontend/@/package.json", "r") as f:
            content = f.read()
        
        if "vite" in content.lower():
            print("✅ Vite configuration found")
        else:
            print("❌ Vite configuration not found")
            return False
        
        # Check if API service exists
        if os.path.exists("Frontend/@/src/services/api.js"):
            print("✅ API service found")
        else:
            print("❌ API service not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking frontend config: {e}")
        return False

def main():
    """Run all deployment checks."""
    print("🚀 Render.com Deployment Check")
    print("=" * 50)
    
    checks = [
        ("Project Structure", check_directory_structure),
        ("Render.yaml Configuration", check_render_yaml),
        ("Backend Configuration", check_backend_config),
        ("Frontend Configuration", check_frontend_config)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n🔬 Running {check_name} check...")
        result = check_func()
        results.append((check_name, result))
    
    # Summary
    print("\n📊 Deployment Check Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED!")
        print("Your project is ready for Render.com deployment!")
        print("\nNext steps:")
        print("1. Push to GitHub: git add . && git commit -m 'Deploy to Render' && git push")
        print("2. Go to render.com and create a new Blueprint")
        print("3. Connect your GitHub repository")
        print("4. Deploy!")
    else:
        print(f"\n⚠️  {total - passed} checks failed.")
        print("Please fix the issues above before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
