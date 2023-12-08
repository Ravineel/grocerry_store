from flask import current_app as app, jsonify, make_response, request
from flask_restful import Resource, reqparse, marshal_with, fields
from Application.models import Order,Product
from Application.db import db
from Application.error_handling import BusinessValidationError
from Application.middleware import level_required
from datetime import datetime
import uuid







# Request Body: {'products': [
  # {'product_id': 1, 'product_name': 'Dummy Product', 'category_name': 'Breads', 'category_id': 2, 'rate': 25.99, 'unit': 'pieces', 'quantity': 2, 'total': 51.98},
  # {'product_id': 2, 'product_name': 'Dummy Product 2sda', 'category_name': 'Breads', 'category_id': 2, 'rate': 25.99, 'unit': 'pieces', 'quantity': 2, 'total': 51.98},
  # {'product_id': 3, 'product_name': 'Dummy Product 3', 'category_name': 'Dairy', 'category_id': 1, 'rate': 5.99, 'unit': 'pieces', 'quantity': 1, 'total': 5.99}
  # ]}

class CheckoutApi(Resource):
  
  @level_required(1)
  def post(current_user,self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('products', type=dict, action="append", required=True, help="products field is required")
      args = parser.parse_args()
      products = args['products']
      id = str(uuid.uuid4())[:8]
      order_id = "PO-"+id+str(current_user.id)
      for product in products:
        print(product)
        total = 0
        product_id = product['product_id']
        product_name = product['product_name']
        qty = product['quantity']
        rate = product['rate']
        unit = product['unit']
        total = qty * rate
        
        # Check if product exists 
        product = Product.query.filter_by(product_id=product_id).first()
        if not product:
          raise BusinessValidationError(400, "PRODUCT_NOT_FOUND", "Product not found")
        # Check if product  has enough quantity mention product name
        if product.qty < qty:
          raise BusinessValidationError(400, "PRODUCT_NOT_ENOUGH", "Product "+product_name+" does not have enough quantity")
        # Update product quantity
        product.qty = product.qty - qty
        # Create order
        order = Order(
          order_id=order_id,
          order_date=datetime.now(),
          user_id=current_user.id,
          product_id=product_id,
          qty=qty,
          rate=rate,
          unit=unit,
          total=total,
          create_date=datetime.now()
          )
        
        db.session.add(order)
      db.session.commit()
      return make_response(jsonify({
        "success":True,
        "message":"Order placed successfully",
        "order_id":order_id
        }), 200)
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))