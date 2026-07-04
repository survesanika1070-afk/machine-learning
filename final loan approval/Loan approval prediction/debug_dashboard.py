#!/usr/bin/env python3
"""
Debug script to identify dashboard issues
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, LoanApplication
from flask import session

def test_dashboard_components():
    """Test all components needed for dashboard"""
    print("🔍 Testing Dashboard Components")
    print("=" * 40)
    
    with app.test_client() as client:
        with app.app_context():
            # Test 1: Check if users exist
            print("1. Testing User Database...")
            users = User.query.all()
            print(f"   Found {len(users)} users:")
            for user in users:
                print(f"   - {user.username} (ID: {user.id}, Admin: {user.is_admin})")
            
            # Test 2: Check if applications exist
            print("\n2. Testing Applications Database...")
            applications = LoanApplication.query.all()
            print(f"   Found {len(applications)} applications")
            
            # Test 3: Test dashboard route without login
            print("\n3. Testing Dashboard Route (No Login)...")
            response = client.get('/dashboard', follow_redirects=False)
            print(f"   Status Code: {response.status_code}")
            if response.status_code == 302:
                print("   ✅ Correctly redirects to login when not authenticated")
            else:
                print(f"   ❌ Unexpected response: {response.data.decode()}")
            
            # Test 4: Test login
            print("\n4. Testing Login...")
            login_data = {'username': 'admin', 'password': 'admin123'}
            response = client.post('/login', data=login_data, follow_redirects=True)
            print(f"   Login Status: {response.status_code}")
            
            # Test 5: Test dashboard with admin login
            print("\n5. Testing Dashboard (Admin Login)...")
            response = client.get('/dashboard', follow_redirects=False)
            print(f"   Status Code: {response.status_code}")
            if response.status_code == 302:
                print("   ✅ Admin correctly redirected to admin dashboard")
            else:
                print(f"   ❌ Unexpected response: {response.data.decode()}")
            
            # Test 6: Create a regular user and test
            print("\n6. Testing Regular User...")
            # Check if regular user exists, create if not
            regular_user = User.query.filter_by(username='testuser').first()
            if not regular_user:
                regular_user = User(username='testuser', email='test@example.com')
                regular_user.set_password('test123')
                db.session.add(regular_user)
                db.session.commit()
                print("   Created test user: testuser / test123")
            
            # Logout admin
            client.get('/logout')
            
            # Login as regular user
            login_data = {'username': 'testuser', 'password': 'test123'}
            response = client.post('/login', data=login_data, follow_redirects=True)
            print(f"   Regular user login status: {response.status_code}")
            
            # Test dashboard with regular user
            response = client.get('/dashboard', follow_redirects=False)
            print(f"   Dashboard status for regular user: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Regular user can access dashboard")
                # Check if template renders correctly
                if b'Simra Kazi' in response.data or b'Welcome' in response.data:
                    print("   ✅ Dashboard template renders correctly")
                else:
                    print("   ❌ Dashboard template may have issues")
                    print(f"   Response preview: {response.data.decode()[:200]}...")
            else:
                print(f"   ❌ Regular user dashboard error: {response.data.decode()}")
            
            # Test 7: Check template file exists
            print("\n7. Testing Template Files...")
            import os
            template_path = 'templates/dashboard.html'
            if os.path.exists(template_path):
                print(f"   ✅ {template_path} exists")
                with open(template_path, 'r') as f:
                    content = f.read()
                    if 'user' in content and 'applications' in content:
                        print("   ✅ Template contains required variables")
                    else:
                        print("   ❌ Template missing required variables")
            else:
                print(f"   ❌ {template_path} missing")

def fix_common_issues():
    """Fix common dashboard issues"""
    print("\n🔧 Attempting to Fix Common Issues...")
    print("=" * 40)
    
    with app.app_context():
        # Ensure admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@loanapproval.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Created admin user")
        
        # Ensure test user exists
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            test_user = User(username='testuser', email='test@example.com')
            test_user.set_password('test123')
            db.session.add(test_user)
            db.session.commit()
            print("✅ Created test user")

if __name__ == "__main__":
    try:
        fix_common_issues()
        test_dashboard_components()
        print("\n🎯 Debug complete!")
        print("\n📝 Next Steps:")
        print("1. Use 'admin' / 'admin123' for admin access")
        print("2. Use 'testuser' / 'test123' for regular user access")
        print("3. Access: http://localhost:5000")
    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback
        traceback.print_exc()
