from flask import current_app as app, jsonify, make_response
from flask_restful import Resource, reqparse,marshal_with, fields
from werkzeug.security import check_password_hash
from Application.models import User, Category, CategoryRequest
from Application.db import db
from Application.error_handling import BusinessValidationError, TokenExpiredError, TokenInvalidError, InsufficientLevelError
from Application.middleware import level_required
from datetime import datetime, timedelta
import jwt





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
        


class CategoryAdminAPI(Resource):
  
  @level_required(min_level=3)
  def post(self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('category_name', type=str, required=True)
      parser.add_argument('description', type=str, required=True)
      args = parser.parse_args()
      category_name = args['category_name']
      description = args['description']
      category = Category.query.filter_by(category_name=category_name).first()
      if category:
        raise BusinessValidationError(400, "CATEGORY_ALREADY_EXISTS", "Category already exists!")
      category = Category(category_name=category_name, description=description)
      db.session.add(category)
      db.session.commit()
      return {"message": "Category created successfully!"}, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
  
  
  @level_required(min_level=3)
  def patch(self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('category_id', type=int, required=True)
      parser.add_argument('category_name', type=str, required=True)
      parser.add_argument('description', type=str, required=True)
      args = parser.parse_args()
      category_id = args['category_id']
      category_name = args['category_name']
      description = args['description']
      category = Category.query.filter_by(category_id=category_id).first()
      if not category:
        raise BusinessValidationError(400, "CATEGORY_NOT_FOUND", "Category not found!")
      category.category_name = category_name
      category.description = description
      db.session.commit()
      return {"message": "Category updated successfully!"}, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))