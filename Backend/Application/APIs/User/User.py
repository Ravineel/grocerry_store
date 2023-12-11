from flask import current_app as app, jsonify, make_response, request
from flask_restful import Resource, reqparse, marshal_with, fields
from Application.models import User, Product, Category, Order
from Application.db import db
from Application.error_handling import BusinessValidationError
from Application.middleware import level_required
from datetime import datetime


manager_list_fields = {
  "id": fields.Integer,
  "email": fields.String,
  "first_name": fields.String,
  "last_name": fields.String,
  "role": fields.Integer,
  "is_manager_active": fields.Boolean,
  "account_created_at": fields.String
}



class userManagerRole(Resource):
  
  @level_required(3)
  @marshal_with(manager_list_fields)
  def get(current_app,self):
    try:
      users = User.query.filter_by(role=2).all()
      if not users:
        raise BusinessValidationError(400, "MANAGER_NOT_FOUND", "Manager not found")
      return users,200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    
  @level_required(3)
  def patch(current_app,self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('manager_id', type=int, required=True)
      parser.add_argument('is_manager_active', type=bool, required=True)
      
      args = parser.parse_args()
      
      manager_id = args['manager_id']
      is_manager_active = args['is_manager_active']
      
      manager = User.query.filter_by(id=manager_id).first()
      
      if not manager:
        raise BusinessValidationError(400, "MANAGER_NOT_FOUND", "Manager not found")
      
      manager.is_manager_active = is_manager_active
      db.session.commit()
      
      return make_response(jsonify({
        "success":True,
        "message":"Manager role updated successfully"
        }), 200)
    
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    

manager_data_fields = {
  "active_managers_count": fields.Integer,
  "inactive_managers_count": fields.Integer,
  "total_managers_count": fields.Integer,
}

class managerData(Resource):
  
  @level_required(3)
  @marshal_with(manager_data_fields)
  def get(current_user,self):
    try:
      active_managers_count = User.query.filter_by(role=2,is_manager_active=True).count()
      inactive_managers_count = User.query.filter_by(role=2,is_manager_active=False).count()
      total_managers_count = User.query.filter_by(role=2).count()
      
      data= {
        "active_managers_count":active_managers_count,
        "inactive_managers_count":inactive_managers_count,
        "total_managers_count":total_managers_count
      }
      return data,200
      
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)


data_count ={
  "total_users": fields.Integer,
  "total_products": fields.Integer,
  "total_categories": fields.Integer,
  "total_orders": fields.Integer,
}

class dataCount(Resource):
  
  @level_required(3)
  @marshal_with(data_count)
  def get(current_user,self):
    try:
      total_users = User.query.filter_by(role=1).count()
      total_products = Product.query.count()
      total_categories = Category.query.count()
      total_orders = Order.query.count()
      
      data= {
        "total_users":total_users,
        "total_products":total_products,
        "total_categories":total_categories,
        "total_orders":total_orders
      }
      return data,200
      
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)