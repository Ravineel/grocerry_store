from main import app
from Application.security import datastore
from Application.models import db, Role
from flask_security import hash_password
from werkzeug.security import generate_password_hash


with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name="admin", description="User is an admin")
    datastore.find_or_create_role(
        name="user", description="User for the application")
    db.session.commit()
    if not datastore.find_user(email="admin@email.com"):
        datastore.create_user(
            email="admin@email.com", username="admin",first_name='admin',last_name='',password_hash=generate_password_hash("admin"), roles=["admin"])
    if not datastore.find_user(email="user1@email.com"):
        datastore.create_user(
            email="user1@email.com",  username="user01",first_name='user',last_name='', password_hash=generate_password_hash("user1"), roles=["user"])
    if not datastore.find_user(email="user2@email.com"):
        datastore.create_user(
            email="user2@email.com",  username="user02",first_name='user02',last_name='', password_hash=generate_password_hash("user2"), roles=["user"])
    db.session.commit()
    print("Done")