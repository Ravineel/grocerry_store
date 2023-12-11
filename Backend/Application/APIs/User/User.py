from flask import current_app as app, jsonify, make_response, request
from flask_restful import Resource, reqparse, marshal_with, fields
from Application.models import User
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
    
# get user count siguped by month api


user_count_list = {
                   
  "user_count": fields.Integer,
  "month": fields.String,
  "year": fields.String,
}


class userCount(Resource):
    @level_required(3)
    @marshal_with(user_count_list)
    def get(current_app,self):
      pass