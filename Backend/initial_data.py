from main import app

from Application.db import db
from Application.models import User, Category, Product, Order



with app.app_context():
    print("Creating tables and initial data...")
    
    db.create_all()
    
    print("Tables created.")
    
    # Create initial data
    print("Adding initial data...")
    
    print("Adding Admin User...")
    admin_user = User(
        username='admin',
        password='admin_password',  # Make sure to hash the password in a real-world scenario
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        role=2,
        account_created_at='2023-01-01',
        jwt_token=None  # You might want to handle JWT tokens differently
    )
    
    print("Adding Normal Users...")

    normal_user1 = User(
        username='user1',
        password='user1_password',
        email='user1@example.com',
        first_name='User',
        last_name='One',
        role=1,
        account_created_at='2023-01-02',
        jwt_token=None
    )

    normal_user2 = User(
        username='user2',
        password='user2_password',
        email='user2@example.com',
        first_name='User',
        last_name='Two',
        role=1,
        account_created_at='2023-01-03',
        jwt_token=None
    )
    
    guest_user1 = User(
        username='user3',
        password='user3_password',
        email='user3@example.com',
        first_name='User',
        last_name='Guest',
        role=0,
        account_created_at='2023-01-03',
        jwt_token=None
    )

    # Add data to the session
    db.session.add_all([admin_user, normal_user1, normal_user2, guest_user1])

    
    print("Users added.")
    # Commit the changes
    db.session.commit()
    print("Tables created and initial data added.")
