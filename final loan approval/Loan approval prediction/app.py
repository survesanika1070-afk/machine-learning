from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loan_approval.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    loan_applications = db.relationship('LoanApplication', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Loan Application model
class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    income = db.Column(db.Float, nullable=False)
    employment_status = db.Column(db.String(50), nullable=False)
    credit_history = db.Column(db.Float, nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    property_area = db.Column(db.String(50), nullable=False)
    prediction_result = db.Column(db.String(20), nullable=False)
    prediction_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Load or create ML model
def load_or_create_model():
    model_path = 'models/loan_model.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    else:
        # Create a simple model for demonstration
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        
        # Sample training data (in production, you'd use real data)
        np.random.seed(42)
        n_samples = 1000
        
        X = pd.DataFrame({
            'age': np.random.randint(21, 70, n_samples),
            'income': np.random.uniform(10000, 100000, n_samples),
            'credit_history': np.random.uniform(0.3, 1.0, n_samples),
            'loan_amount': np.random.uniform(10000, 500000, n_samples),
            'loan_term': np.random.randint(12, 360, n_samples),
            'gender_male': np.random.choice([0, 1], n_samples),
            'employment_employed': np.random.choice([0, 1], n_samples),
            'property_semiurban': np.random.choice([0, 1], n_samples),
            'property_urban': np.random.choice([0, 1], n_samples)
        })
        
        # Simple rule-based labels for demonstration
        y = ((X['credit_history'] > 0.6) & 
             (X['income'] > 30000) & 
             (X['loan_amount'] < X['income'] * 5)).astype(int)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Save the model
        os.makedirs('models', exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        return model

# Load the model
model = load_or_create_model()

def preprocess_input(data):
    """Preprocess input data for ML model"""
    processed = {
        'age': int(data['age']),
        'income': float(data['income']),
        'credit_history': float(data['credit_history']),
        'loan_amount': float(data['loan_amount']),
        'loan_term': int(data['loan_term']),
        'gender_male': 1 if data['gender'].lower() == 'male' else 0,
        'employment_employed': 1 if data['employment_status'].lower() == 'employed' else 0,
        'property_semiurban': 1 if data['property_area'].lower() == 'semiurban' else 0,
        'property_urban': 1 if data['property_area'].lower() == 'urban' else 0
    }
    return pd.DataFrame([processed])

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return render_template('signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!')
            return render_template('signup.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    
    user = User.query.get(session['user_id'])
    applications = LoanApplication.query.filter_by(user_id=user.id).order_by(LoanApplication.created_at.desc()).all()
    
    return render_template('dashboard.html', user=user, applications=applications)

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session or session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get form data
        data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'income': request.form['income'],
            'employment_status': request.form['employment_status'],
            'credit_history': request.form['credit_history'],
            'loan_amount': request.form['loan_amount'],
            'loan_term': request.form['loan_term'],
            'property_area': request.form['property_area']
        }
        
        # Preprocess and predict
        processed_data = preprocess_input(data)
        prediction = model.predict(processed_data)[0]
        prediction_proba = model.predict_proba(processed_data)[0]
        
        result = 'Approved' if prediction == 1 else 'Not Approved'
        score = float(prediction_proba[1]) if prediction == 1 else float(prediction_proba[0])
        
        # Save application
        application = LoanApplication(
            user_id=session['user_id'],
            name=data['name'],
            age=int(data['age']),
            gender=data['gender'],
            income=float(data['income']),
            employment_status=data['employment_status'],
            credit_history=float(data['credit_history']),
            loan_amount=float(data['loan_amount']),
            loan_term=int(data['loan_term']),
            property_area=data['property_area'],
            prediction_result=result,
            prediction_score=score
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash(f'Loan Application Submitted! Result: {result} (Confidence: {score:.2%})')
        
    except Exception as e:
        flash(f'Error processing application: {str(e)}')
    
    return redirect(url_for('dashboard'))

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    users = User.query.all()
    applications = LoanApplication.query.order_by(LoanApplication.created_at.desc()).all()
    
    return render_template('admin.html', users=users, applications=applications)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
