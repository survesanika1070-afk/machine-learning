#!/usr/bin/env python3
"""
Test script to verify all components are properly connected
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from werkzeug.security import generate_password_hash, check_password_hash
        import pickle
        import numpy as np
        import pandas as pd
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_connection():
    """Test database connection and models"""
    print("\nTesting database connection...")
    try:
        from app import app, db, User, LoanApplication
        
        with app.app_context():
            # Check if tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ Database tables: {tables}")
            
            # Test User model
            user_count = User.query.count()
            print(f"✅ Users in database: {user_count}")
            
            # Test LoanApplication model
            app_count = LoanApplication.query.count()
            print(f"✅ Loan applications in database: {app_count}")
            
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_templates():
    """Test if all template files exist"""
    print("\nTesting template files...")
    templates = [
        'templates/base.html',
        'templates/index.html',
        'templates/signup.html',
        'templates/login.html',
        'templates/dashboard.html',
        'templates/admin.html'
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"✅ {template}")
        else:
            print(f"❌ {template} missing")
            return False
    return True

def test_static_files():
    """Test if static files exist"""
    print("\nTesting static files...")
    static_files = [
        'static/css/style.css',
        'static/js/script.js'
    ]
    
    for file in static_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            return False
    return True

def test_ml_model():
    """Test ML model loading"""
    print("\nTesting ML model...")
    try:
        from app import load_or_create_model
        model = load_or_create_model()
        print(f"✅ ML model loaded: {type(model).__name__}")
        return True
    except Exception as e:
        print(f"❌ ML model error: {e}")
        return False

def test_flask_app():
    """Test Flask app configuration"""
    print("\nTesting Flask app...")
    try:
        from app import app
        
        # Check routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.methods} {rule.rule}")
        
        print(f"✅ Flask app configured with {len(routes)} routes:")
        for route in routes[:10]:  # Show first 10 routes
            print(f"   {route}")
        if len(routes) > 10:
            print(f"   ... and {len(routes) - 10} more routes")
        
        return True
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def test_directory_structure():
    """Test if directory structure is correct"""
    print("\nTesting directory structure...")
    directories = [
        'templates',
        'static',
        'static/css',
        'static/js',
        'static/images',
        'models'
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ missing")
            return False
    return True

def main():
    """Run all tests"""
    print("=" * 50)
    print("🔍 Testing Loan Approval System Connections")
    print("=" * 50)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Template Files", test_templates),
        ("Static Files", test_static_files),
        ("Python Imports", test_imports),
        ("Database Connection", test_database_connection),
        ("ML Model", test_ml_model),
        ("Flask App", test_flask_app)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems are ready! The application should work perfectly.")
    else:
        print("⚠️  Some issues found. Please check the failed tests above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
