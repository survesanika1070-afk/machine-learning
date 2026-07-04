from app import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@loanapproval.com',
                is_admin=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("Admin user already exists!")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
