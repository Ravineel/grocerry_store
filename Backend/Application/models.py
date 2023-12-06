
from flask_login import UserMixin
from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app



class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    role=db.Column(db.String, nullable=False)
    account_created_at = db.Column(db.String, nullable=False)
    jwt_token = db.Column(db.String, nullable=True)

    
    def get_id(self):
      return self.id
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
  __tablename__ = 'category'
  category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  category_name = db.Column(db.String(50), nullable=False, unique=True)
  description = db.Column(db.String(50))
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())

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
  create_date = db.Column(db.DateTime, server_default=db.func.now())
  last_update_date = db.Column(db.DateTime, server_default=db.func.now())

class Order(db.Model):
  __tablename__ = 'order'
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



