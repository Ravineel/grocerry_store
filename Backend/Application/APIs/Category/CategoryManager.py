from flask import current_app as app, jsonify, make_response
from flask_restful import Resource, reqparse,marshal_with, fields
from werkzeug.security import check_password_hash
from Application.models import User, Category, CategoryRequest
from Application.db import db
from Application.error_handling import BusinessValidationError
from Application.middleware import level_required
from datetime import datetime, timedelta



category_request_fields = {
  'category_id': fields.Integer,
  'category_name': fields.String,
  'description': fields.String,
  'type': fields.String,
  'request_status': fields.String,
  'request_by': fields.Integer,
  'create_date': fields.DateTime(dt_format='rfc822'),
  'last_update_date': fields.DateTime(dt_format='rfc822'),
  'id': fields.Integer,
  'approved_by': fields.Integer,
  'approved_date': fields.DateTime(dt_format='rfc822'),
  'approved_by_name': fields.String,
  
}
  

class RequestCategoryRequestByManagerAPI(Resource):
  
  @level_required(2)
  @marshal_with(category_request_fields)
  def get(current_user, self):
    try:
      
      
      user_id = current_user.id

      
      category_requests = CategoryRequest.query.outerjoin(User, CategoryRequest.approved_by == User.id)\
        .add_columns(
          CategoryRequest.category_id,CategoryRequest.category_name, CategoryRequest.description, CategoryRequest.type, 
          CategoryRequest.request_status, CategoryRequest.request_by, CategoryRequest.create_date, 
          CategoryRequest.last_update_date, CategoryRequest.id, CategoryRequest.approved_by, 
          CategoryRequest.approved_date, (User.first_name + ' ' + User.last_name).label('approved_by_name'))\
        .filter(CategoryRequest.request_by==user_id)\
        .all()        


      return category_requests, 200
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))

  @level_required(2)
  def post(current_user, self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('category_name', type=str, required=True)
      parser.add_argument('category_id', type=str, required=False)
      parser.add_argument('description', type=str, required=True)
      parser.add_argument('type', type=str, required=True)
      args = parser.parse_args()
      category_name = args['category_name']
      description = args['description']
      type = args['type']
      created_by = current_user.id
      
      category = Category.query.filter_by(category_name=category_name).first()
      if category and type == "CREATE":
        raise BusinessValidationError(400, "CATEGORY_ALREADY_EXISTS", "Category already exists!")
      
      if not category and type == "UPDATE":
        raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
      
      if not category and type == "DELETE":
        raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
      
      if not category and type == "CREATE":
        category_request = CategoryRequest(category_name=category_name, description=description, type=type, request_status="PENDING", request_by=created_by)
      else:
         category_request = CategoryRequest(category_id=args['category_id'], category_name=category_name, description=description, type=type, request_status="PENDING", request_by=created_by)
      
      db.session.add(category_request)
      db.session.commit()
      return {"message": "Category request created successfully!", "success":"true"}, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    
