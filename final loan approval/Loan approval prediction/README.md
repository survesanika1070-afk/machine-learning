# Loan Approval Prediction Web Application

A comprehensive web application for loan approval prediction using machine learning, built with Flask (Python) for the backend and HTML/CSS/JavaScript for the frontend.

## Features

- **User Authentication**: Secure signup and login system
- **Loan Application Form**: Comprehensive form with all required fields
- **ML Prediction**: Random Forest model for loan approval prediction
- **User Dashboard**: View application history and submit new applications
- **Admin Dashboard**: Manage users and view all applications
- **Responsive Design**: Modern UI using Bootstrap 5
- **Database Storage**: SQLite database for user and application data

## Project Structure

```
Loan approval prediction/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── signup.html     # Signup page
│   ├── login.html      # Login page
│   ├── dashboard.html  # User dashboard
│   └── admin.html      # Admin dashboard
├── static/              # Static files
│   ├── css/
│   │   └── style.css   # Custom CSS styles
│   ├── js/
│   │   └── script.js   # JavaScript functionality
│   └── images/         # Image files
└── models/              # ML model files
```

## Installation and Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

This will create the SQLite database and an admin user with:
- Username: `admin`
- Password: `admin123`

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### For Regular Users:

1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Use your credentials to access the system
3. **Dashboard**: 
   - View your application history
   - Submit new loan applications
   - See prediction results with confidence scores

### For Administrators:

1. **Login**: Use admin credentials (admin/admin123)
2. **Admin Dashboard**:
   - View all registered users
   - Monitor all loan applications
   - See detailed statistics and trends

## Loan Application Form Fields

- **Full Name**: Applicant's full name
- **Age**: Applicant's age (18-100)
- **Gender**: Male or Female
- **Annual Income**: Annual income in USD
- **Employment Status**: Employed, Self-Employed, or Unemployed
- **Credit History**: Credit score (0.0-1.0)
- **Loan Amount**: Requested loan amount in USD
- **Loan Term**: Loan duration in months (12-360)
- **Property Area**: Urban, Semiurban, or Rural

## Machine Learning Model

The application uses a Random Forest classifier trained on sample data. The model considers:

- Credit history score
- Income level
- Loan amount relative to income
- Employment status
- Property location
- Age and other demographic factors

The model provides:
- **Prediction**: Approved or Not Approved
- **Confidence Score**: Probability percentage

## Technical Details

### Backend Technologies:
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Werkzeug**: Password hashing
- **Scikit-learn**: Machine learning
- **Pandas**: Data processing
- **NumPy**: Numerical operations

### Frontend Technologies:
- **Bootstrap 5**: UI framework
- **Font Awesome**: Icons
- **JavaScript**: Form validation and interactions
- **CSS3**: Custom styling and animations

### Database:
- **SQLite**: Lightweight database for development
- **Models**: User and LoanApplication tables

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Input validation and sanitization
- CSRF protection (can be enhanced)
- SQL injection prevention through ORM

## Future Enhancements

- Email notifications for application status
- Advanced analytics and reporting
- File upload for document verification
- API endpoints for mobile app integration
- Multi-language support
- Role-based access control
- Audit logging

## Troubleshooting

### Common Issues:

1. **Database Error**: Run `python init_db.py` to initialize the database
2. **Port Already in Use**: Change port in `app.py` or stop other services
3. **Dependencies Missing**: Ensure all requirements are installed
4. **Model Not Found**: The app will auto-create a model on first run

### Development Tips:

- Use `debug=True` for development (change in `app.py`)
- Check browser console for JavaScript errors
- Monitor Flask console for backend errors
- Use Chrome DevTools for responsive testing

## License

This project is for educational purposes. Feel free to modify and use as needed.

## Contact

For questions or issues, please check the troubleshooting section or create an issue in the repository.
