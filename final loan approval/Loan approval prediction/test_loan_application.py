#!/usr/bin/env python3
"""
Test script to submit a loan application
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, LoanApplication

def test_loan_application():
    """Test the complete loan application flow"""
    print("🧪 Testing Loan Application Flow")
    print("=" * 40)
    
    with app.test_client() as client:
        with app.app_context():
            # Login as regular user (Simra-Kazi08 or testuser)
            print("1. Logging in as test user...")
            login_data = {'username': 'testuser', 'password': 'test123'}
            response = client.post('/login', data=login_data, follow_redirects=True)
            print(f"   Login status: {response.status_code}")
            
            # Submit loan application
            print("\n2. Submitting loan application...")
            application_data = {
                'name': 'Simra Kazi',
                'age': '20',
                'gender': 'Female',
                'income': '75000',
                'employment_status': 'Employed',
                'credit_history': '1',
                'loan_amount': '25000',
                'loan_term': '60',
                'property_area': 'Urban'
            }
            
            response = client.post('/predict', data=application_data, follow_redirects=True)
            print(f"   Application status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Application submitted successfully!")
                
                # Check if application was saved to database
                applications = LoanApplication.query.filter_by(name='Simra Kazi').all()
                if applications:
                    loan_app = applications[-1]  # Get the most recent
                    print(f"   ✅ Application saved to database")
                    print(f"   - Name: {loan_app.name}")
                    print(f"   - Loan Amount: ${loan_app.loan_amount}")
                    print(f"   - Prediction: {loan_app.prediction_result}")
                    print(f"   - Confidence: {loan_app.prediction_score:.2%}" if loan_app.prediction_score else "N/A")
                else:
                    print("   ❌ Application not found in database")
            else:
                print(f"   ❌ Application failed: {response.data.decode()}")
            
            # Test dashboard display
            print("\n3. Testing dashboard display...")
            response = client.get('/dashboard')
            if response.status_code == 200:
                if b'Simra Kazi' in response.data:
                    print("   ✅ Application appears in dashboard")
                else:
                    print("   ❌ Application not visible in dashboard")
            else:
                print(f"   ❌ Dashboard error: {response.status_code}")

if __name__ == "__main__":
    try:
        test_loan_application()
        print("\n🎉 Loan application test complete!")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
