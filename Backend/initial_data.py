from main import app

from Application.db import db
from Application.models import User, Category, Product, Order
from datetime import date


with app.app_context():
    print("Creating tables and initial data...")
    
    db.create_all()
    
    print("Tables created.")
    
    # Create initial data
    print("Adding initial data...")
    print(date.fromisoformat('2023-01-01'))
    print("Adding Admin User...")
    admin_user = User(
      
        password='admin_password',  
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        role=3,
        account_created_at=date.fromisoformat('2023-01-01'),
        jwt_token=None 
    )
    print("Adding Manger user.")
    
    manager_user1 = User(
        
        password='manager1_password',
        email='mager1@gmail.com',
        first_name='Manager',
        last_name='One',
        role=2,
        account_created_at=date.fromisoformat('2023-01-01'),
        jwt_token=None
    )    
    
    
    print("Adding Normal Users...")

    normal_user1 = User(
   
        password='user1_password',
        email='user1@example.com',
        first_name='User',
        last_name='One',
        role=1,
        account_created_at=date.fromisoformat('2023-01-01'),
        jwt_token=None
    )

    normal_user2 = User(
        password='user2_password',
        email='user2@example.com',
        first_name='User',
        last_name='Two',
        role=1,
        account_created_at=date.fromisoformat('2023-01-01'),
        jwt_token=None
    )
    
    
    # Add data to the session
    db.session.add_all([admin_user, manager_user1, normal_user1, normal_user2])

    
    print("Users added.")
    # Commit the changes
    db.session.commit()
    print("Tables created and initial data added.")
