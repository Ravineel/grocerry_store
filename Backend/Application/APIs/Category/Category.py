from flask import current_app as app, jsonify, make_response
from flask_restful import Resource, reqparse,marshal_with, fields
from werkzeug.security import check_password_hash
from Application.models import User, Category, CategoryRequest
from Application.db import db
from Application.error_handling import BusinessValidationError, TokenExpiredError, TokenInvalidError, InsufficientLevelError
from Application.middleware import level_required
from datetime import date
from sqlalchemy.orm import aliased





category_fields = {
  'category_id': fields.Integer,
  'category_name': fields.String,
  'description': fields.String,
  'create_date': fields.DateTime,
}

class CategoryGeneralAPI(Resource):
  
  @marshal_with(category_fields)
  def get(self):
    try:
      categories = Category.query.all()
      return categories, 200
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
     
        
class CategoryByIdAPI(Resource):
  
    @marshal_with(category_fields)
    def get(self, category_id):
      try:
        category = Category.query.filter_by(category_id=category_id).first()
        if not category:
          raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
        return category, 200
      except BusinessValidationError as e:
        raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
      except Exception as e:
        raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))


class CategoryAdminAPI(Resource):
  
  @level_required(3)
  def post(current_user, self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('category_name', type=str, required=True)
      parser.add_argument('description', type=str, required=True)
      args = parser.parse_args()
      
      category_name = args['category_name']
      description = args['description']
      created_by = current_user.id
      
      category = Category.query.filter_by(category_name=category_name).first()
      
      if category:
        raise BusinessValidationError(400, "CATEGORY_ALREADY_EXISTS", "Category already exists!")
      
      category = Category(category_name=category_name, description=description, create_by=created_by, last_update_by=created_by, create_date=date.today(), last_update_date=date.today())
      db.session.add(category)
      db.session.commit()
      
      return {"message": "Category created successfully!","success":"true"}, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
  
  
  @level_required(3)
  def patch(current_user, self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('category_id', type=int, required=True)
      parser.add_argument('category_name', type=str, required=True)
      parser.add_argument('description', type=str, required=True)
      args = parser.parse_args()
      
      category_id = args['category_id']
      category_name = args['category_name']
      description = args['description']
      updated_by = current_user.id
      
      category = Category.query.filter_by(category_id=category_id).first()
      
      if not category:
        raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
      
      category.category_name = category_name
      category.description = description
      category.last_update_by = updated_by
      category.last_update_date = date.today()
      
      db.session.commit()
      
      return {"message": "Category updated successfully!","success":"true"}, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))

  @level_required(3)
  def delete(current_user, self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('category_id', type=int, required=True)
      args = parser.parse_args()
      
      category_id = args['category_id']
      
      category = Category.query.filter_by(category_id=category_id).first()
      
      if not category:
        raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
      
      db.session.delete(category)
      db.session.commit()
      
      return {"message": "Category deleted successfully!","success":"true"}, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    



category_request_fields={
  'id': fields.Integer,
  'category_id': fields.Integer,
  'category_name': fields.String,
  'description': fields.String,
  'request_by': fields.Integer,
  'request_date': fields.DateTime,
  'request_status': fields.String,
  'create_date': fields.DateTime,
  'type': fields.String,
  'approved_by': fields.Integer,
  'approved_date': fields.DateTime,
  'last_update_by': fields.Integer,
  'last_update_date': fields.DateTime,
  'approved_by_name': fields.String,
  'requested_by_name': fields.String,
}

class CategoryRequestAPI(Resource):
  
  #get all requests
  @level_required(2)
  @marshal_with(category_request_fields)
  def get(current_user, self):
    try:
 
      user_approved_by = aliased(User)
      user_requested_by = aliased(User)
    
      
      category_requests = CategoryRequest.query.outerjoin(user_approved_by, CategoryRequest.approved_by == user_approved_by.id) \
      .outerjoin(user_requested_by, CategoryRequest.request_by == user_requested_by.id) \
      .add_columns(
          CategoryRequest.category_id, CategoryRequest.category_name, CategoryRequest.description, 
          CategoryRequest.type, CategoryRequest.request_status, CategoryRequest.request_by, 
          CategoryRequest.create_date, CategoryRequest.last_update_date, CategoryRequest.id, 
          CategoryRequest.approved_by, CategoryRequest.approved_date, 
          (user_approved_by.first_name + ' ' + user_approved_by.last_name).label('approved_by_name'),
          (user_requested_by.first_name + ' ' + user_requested_by.last_name).label('requested_by_name')
      )\
      .all()
      

      
      return category_requests, 200
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    

  
  @level_required(3)
  def post(current_user, self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('category_id', type=str, required=True)
      parser.add_argument('has_approved', type=str, required=True)
      args = parser.parse_args()
      
      category_id = args['category_id']
      approval = args['has_approved']
      approved_by = current_user.id
      approved_date = date.today()
      
      category_request = CategoryRequest.query.filter_by(id=category_id).first()
     
      if not category_request:
        raise BusinessValidationError(404, "CATEGORY_REQUEST_NOT_FOUND", "Category request not found!")
     
      if approval == "false":
        category_request.request_status = "REJECTED"
        category_request.approved_by = approved_by
        category_request.approved_date = approved_date
        category_request.last_update_date = date.today()
        db.session.commit()
        return {"message": "Category request rejected successfully!"}, 200
      
      elif approval == "true":
        category_request.request_status = "APPROVED"
        category_request.approved_by = approved_by
        category_request.approved_date = approved_date
        category_request.last_update_date = date.today()
        db.session.commit()
        
        if category_request.type == "CREATE":
          category = Category(category_name=category_request.category_name, description=category_request.description, create_by=category_request.request_by, last_update_by=category_request.approved_by, create_date=date.today(),last_update_date=date.today())
          db.session.add(category)
          db.session.commit()
        
        elif category_request.type == "UPDATE":
          category = Category.query.filter_by(category_id=category_request.category_id).first()
          if not category:
            raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
          category.category_name = category_request.category_name
          category.description = category_request.description
          category.last_update_by = category_request.request_by
          category.last_update_date = date.today()
          db.session.commit() 
          
        elif category_request.type == "DELETE":
          category = Category.query.filter_by(category_id=category_request.category_id).first()
          if not category:
            raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
          db.session.delete(category)
          db.session.commit()
  
        return {"message": "Category request approved successfully!"}, 200
      else:
        raise BusinessValidationError(400, "INVALID_REQUEST", "Invalid request!")
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    
