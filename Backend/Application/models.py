from .database import db
from flask import current_app as app
from flask_security  import UserMixin, RoleMixin

class UserRole(db.Model):
  __tablename__ = 'user_role'
  id = db.Column(db.Integer(), primary_key=True)
  user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
  role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
 
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50))
  email = db.Column(db.String(50), nullable=False, unique=True)
  username = db.Column(db.String(50), nullable=False, unique=True)
  password_hash = db.Column(db.String(255), nullable=False)
  fs_uniquifier = db.Column(db.String(255), unique=True)
  token = db.Column(db.String(255), unique=True)
  active = db.Column(db.Boolean, default=False)
  last_login = db.Column(db.DateTime)
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())
  roles = db.relationship('Role', secondary='user_role', backref=db.backref('users', lazy='dynamic'))  
 
class Role(db.Model,RoleMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False, unique=True)
  description = db.Column(db.String(50))
  create_date = db.Column(db.DateTime, server_default=db.func.now())


class Category(db.Model):
  category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  category_name = db.Column(db.String(50), nullable=False, unique=True)
  description = db.Column(db.String(50))
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())

class Product(db.Model):
  product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  product_name = db.Column(db.String(50), nullable=False, unique=True)
  description = db.Column(db.String(50))
  category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
  qty = db.Column(db.Integer, nullable=False)
  rate = db.Column(db.Float, nullable=False)
  unit = db.Column(db.String(50), nullable=False)
  active = db.Column(db.Boolean, default=True)
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  order_id = db.Column(db.Integer, nullable=False)
  order_date = db.Column(db.DateTime, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
  qty = db.Column(db.Integer, nullable=False)
  rate = db.Column(db.Float, nullable=False)
  unit = db.Column(db.String(50), nullable=False)
  total = db.Column(db.Float, nullable=False)
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())



