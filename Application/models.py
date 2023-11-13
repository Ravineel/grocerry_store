from .database import db
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
  __tablename__ = 'user'
  user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50))
  email = db.Column(db.String(50), nullable=False, unique=True)
  username = db.Column(db.String(50), nullable=False, unique=True)
  password_hash = db.Column(db.String(128), nullable=False)
  token = db.Column(db.String(128), unique=True)
  active = db.Column(db.Boolean, default=False)
  last_login = db.Column(db.DateTime)
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())
  roles = db.relationship('Role', secondary='user_role', backref=db.backref('users', lazy='dynamic'))  
  orders = db.relationship('Order', backref='user', lazy='dynamic')  


class Category(db.Model):
  __tablename__ = 'category'
  category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  category_name = db.Column(db.String(50), nullable=False, unique=True)
  description = db.Column(db.String(50))
  create_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())
  products = db.relationship('Product', backref='category', lazy='dynamic')

class Product(db.Model):
  __tablename__ = 'product'
  product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  product_name = db.Column(db.String(50), nullable=False, unique=True)
  description = db.Column(db.String(50))
  category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
  qty = db.Column(db.Integer, nullable=False)
  rate = db.Column(db.Float, nullable=False)
  unit = db.Column(db.String(50), nullable=False)
  active = db.Column(db.Boolean, default=True)
  create_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())
  orders = db.relationship('Order', backref='product', lazy='dynamic')

class Order(db.Model):
  __tablename__ = 'order'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  order_id = db.Column(db.Integer, nullable=False)
  order_date = db.Column(db.DateTime, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
  qty = db.Column(db.Integer, nullable=False)
  rate = db.Column(db.Float, nullable=False)
  unit = db.Column(db.String(50), nullable=False)
  total = db.Column(db.Float, nullable=False)
  create_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())

class Role(db.Model):
  __tablename__ = 'role'
  role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  role_name = db.Column(db.String(50), nullable=False, unique=True)
  description = db.Column(db.String(50))
  create_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())

class UserRole(db.Model):
  __tablename__ = 'user_role'
  user_role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
  role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), primary_key=True)
 

