from flask import current_app as app, jsonify, make_response
from flask_restful import Resource, reqparse,marshal_with, fields
from werkzeug.security import check_password_hash
from Application.models import User, Category, CategoryRequest
from Application.db import db
from Application.error_handling import BusinessValidationError, TokenExpiredError, TokenInvalidError, InsufficientLevelError
from Application.middleware import level_required
from datetime import datetime, timedelta
import jwt


from flask import current_app as app, jsonify, make_response
from flask_restful import Resource, reqparse,marshal_with, fields
from werkzeug.security import check_password_hash
from Application.models import User, Category, CategoryRequest
from Application.db import db
from Application.error_handling import BusinessValidationError, TokenExpiredError, TokenInvalidError, InsufficientLevelError
from Application.middleware import level_required
from datetime import datetime, timedelta
import jwt


  

class CreateCategoryRequestByManagerAPI(Resource):

  @level_required(2)
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
      category_request = CategoryRequest(category_name=category_name, description=description, type="CREATE", request_status="PENDING", request_by=created_by)
      db.session.add(category_request)
      db.session.commit()
      return {"message": "Category request created successfully!"}, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    

class UpdateCategoryRequestByManagerAPI(Resource):
  
    @level_required(2)
    def post(current_user, self):
      try:
        parser = reqparse.RequestParser()
        parser.add_argument('category_id', type=int, required=True)
        parser.add_argument('category_name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()
        category_id = args['category_id']
        category_name = args['category_name']
        description = args['description']
        request_by = current_user.id
        
        category = Category.query.filter_by(category_id=category_id).first()
        if not category:
          raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
        category_request = CategoryRequest(category_name=category_name, description=description, type="UPDATE", request_status="PENDING", request_by=request_by)
        db.session.add(category_request)
        db.session.commit()
        return {"message": "Category request created successfully!"}, 200
      except BusinessValidationError as e:
        raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
      except Exception as e:
        raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
      

class DeleteCategoryRequestByManagerAPI(Resource):
    
      @level_required(2)
      def post(current_user, self):
        try:
          parser = reqparse.RequestParser()
          parser.add_argument('category_id', type=int, required=True)
          args = parser.parse_args()
          category_id = args['category_id']
          request_by = current_user.id
          
          category = Category.query.filter_by(category_id=category_id).first()
          if not category:
            raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
          category_request = CategoryRequest(category_name=category.category_name, description=category.description, type="DELETE", request_status="PENDING", request_by=request_by)
          db.session.add(category_request)
          db.session.commit()
          return {"message": "Category request created successfully!"}, 200
        except BusinessValidationError as e:
          raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
        except Exception as e:
          raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))