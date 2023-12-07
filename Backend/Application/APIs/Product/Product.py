from flask import current_app as app, jsonify, make_response
from flask_restful import Resource, reqparse,marshal_with, fields
from werkzeug.security import check_password_hash
from Application.models import User, Category, CategoryRequest, Product
from Application.db import db
from Application.error_handling import BusinessValidationError, TokenExpiredError, TokenInvalidError, InsufficientLevelError
from Application.middleware import level_required
from datetime import datetime, timedelta
import jwt


Product_fields = {
  'product_id': fields.Integer,
  'product_name': fields.String,
  'description': fields.String,
  'create_date': fields.DateTime,
  'category_id': fields.Integer,
  'qty': fields.Integer,
  'rate': fields.Float,
  'unit': fields.String,
  'active': fields.Boolean,
  'manufacturer': fields.String,
  'mfg_date': fields.DateTime,
}

class ProductGeneralAPI(Resource):
  
  @marshal_with(Product_fields)  
  def get(self):
    try:
      products = Product.query.all()
      return products, 200
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    

class ProductByIdAPI(Resource):
    
    @marshal_with(Product_fields)  
    def get(self, product_id):
      try:
        product = Product.query.filter_by(product_id=product_id).first()
        if product is None:
          raise BusinessValidationError(404, "PRODUCT_NOT_FOUND", "Product with id {} not found".format(product_id))
        return product, 200
      except BusinessValidationError as e:
        raise e
      except Exception as e:
        raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
      

class ProductManagerAPI(Resource): #create, update, delete product
  
  @level_required(2)
  def post(current_user,self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('product_name', type=str, required=True)
      parser.add_argument('description', type=str, required=True)
      parser.add_argument('category_id', type=int, required=True)
      parser.add_argument('qty', type=int, required=True)
      parser.add_argument('rate', type=float, required=True)
      parser.add_argument('unit', type=str, required=True)
      parser.add_argument('manufacturer', type=str, required=True)
      parser.add_argument('mfg_date', type=str, required=True)
      args = parser.parse_args()
      
      create_by = current_user.id
      
      product = Product(
        product_name=args['product_name'],
        description=args['description'],
        category_id=args['category_id'],
        qty=args['qty'],
        rate=args['rate'],
        unit=args['unit'],
        manufacturer=args['manufacturer'],
        mfg_date=datetime.strptime(args['mfg_date'], '%d-%m-%Y'),
        create_by=create_by,
        last_update_by=create_by
        
      )
      db.session.add(product)
      db.session.commit()
      return product, 200
    except BusinessValidationError as e:
      raise e
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
  
  @level_required(2)
  def patch(current_user,self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('product_id', type=int, required=True)
      parser.add_argument('product_name', type=str, required=True)
      parser.add_argument('description', type=str, required=True)
      parser.add_argument('category_id', type=int, required=True)
      parser.add_argument('qty', type=int, required=True)
      parser.add_argument('rate', type=float, required=True)
      parser.add_argument('unit', type=str, required=True)
      parser.add_argument('manufacturer', type=str, required=True)
      parser.add_argument('mfg_date', type=str, required=True)
      parser.add_argument('active', type=bool, required=True)
      args = parser.parse_args()
      
      product = Product.query.filter_by(product_id=args['product_id']).first()
      if product is None:
        raise BusinessValidationError(404, "PRODUCT_NOT_FOUND", "Product with id {} not found".format(args['product_id']))
      product.product_name = args['product_name']
      product.description = args['description']
      product.category_id = args['category_id']
      product.qty = args['qty']
      product.rate = args['rate']
      product.unit = args['unit']
      product.manufacturer = args['manufacturer']
      product.mfg_date = datetime.strptime(args['mfg_date'], '%d-%m-%Y')
      product.last_update_date = datetime.now()
      product.last_update_by = current_user.id
      product.active = args['active']
      db.session.commit()
      return product, 200
    except BusinessValidationError as e:
      raise e
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
  
  @level_required(2)
  def delete(current_user,self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('product_id', type=int, required=True)
      args = parser.parse_args()
      
      product = Product.query.filter_by(product_id=args['product_id']).first()
      if product is None:
        raise BusinessValidationError(404, "PRODUCT_NOT_FOUND", "Product with id {} not found".format(args['product_id']))
      db.session.delete(product)
      db.session.commit()
      return {}, 200
    except BusinessValidationError as e:
      raise e
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    
  