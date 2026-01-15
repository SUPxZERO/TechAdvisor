"""Fix admin user password"""
from app import create_app, db
from app.models.user import User

app = create_app('development')

with app.app_context():
    # Delete existing admin if exists
    admin = User.query.filter_by(username='admin').first()
    if admin:
        db.session.delete(admin)
        db.session.commit()
        print("Deleted existing admin user")
    
    # Create new admin with correct password
    admin = User(
        username='admin',
        email='admin@techadvisor.local',
        role='admin',
        is_active=True
    )
    admin.set_password('admin123')
    
    db.session.add(admin)
    db.session.commit()
    
    # Verify
    admin_test = User.query.filter_by(username='admin').first()
    password_ok = admin_test.check_password('admin123')
    
    print(f"Admin user created: {admin_test is not None}")
    print(f"Password verification: {password_ok}")
    print(f"Username: {admin_test.username}")
    print(f"Email: {admin_test.email}")
    print(f"Role: {admin_test.role}")
