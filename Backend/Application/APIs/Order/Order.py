from flask import current_app as app, jsonify, make_response, request
from flask_restful import Resource, reqparse, marshal_with, fields
from Application.models import Order,Product, User
from Application.db import db
from Application.error_handling import BusinessValidationError
from Application.middleware import level_required
from datetime import datetime
import uuid

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
    
    
orders_list = {
    "order_id":fields.String,
    "order_date":fields.DateTime,
    "qty":fields.Integer,
    "rate":fields.Float,
    "unit":fields.String,
    "total":fields.Float,
    "user_name":fields.String,
    "product_name":fields.String
 }   
    

orders_ids_list = {
  "order_id":fields.String,
  "order_date":fields.DateTime,
  "product_count":fields.Integer,
  "total":fields.Float
}

class getAllOrdersIdUserApi(Resource):
  @level_required(1)
  @marshal_with(orders_ids_list)
  def get(current_user,self):
    try:
    
      userid = current_user.user_id
      
      # group by order, get products count and total amount
      orders = Order.query.group_by(Order.order_id)\
        .add_columns(
          Order.order_id, Order.order_date, 
          db.func.count(Order.product_id).label('product_count'), 
          db.func.sum(Order.total).label('total')
          )\
        .filter_by(user_id=userid).all()
      
      
      if not orders:
        raise BusinessValidationError(400, "ORDER_NOT_FOUND", "Order not found")
      return orders, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
  

class getUserOrdersApi(Resource):
  
  @level_required(1)
  @marshal_with(orders_list)
  def get(current_user,self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('order_id', type=str, required=True, help="order_id field is required")
      args = parser.parse_args()
    
      userid = current_user.user_id
      orders = Order.query.outterjoin(User, Order.user_id == User.id).outterjoin(Product, Order.product_id == Product.product_id)\
      .add_columns(
        Order.order_id, Order.order_date, Order.qty, Order.rate, Order.unit, Order.total,
        (User.first_name + " " + User.last_name).label('user_name'), Product.product_name
        ).filter_by(
          Order.user_id == userid
        ).filter_by(
          Order.order_id == args['order_id']
        ).all()
      
      if not orders:
        raise BusinessValidationError(400, "ORDER_NOT_FOUND", "Order not found")
      return orders, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    
    
    
# for admin get all orders by order id, total amount, order date, order_month, order_year, product_count


order_data={
  "order_id":fields.String,
  "order_date":fields.DateTime,
  "order_month":fields.String,
  "order_year":fields.String,
  "product_count":fields.Integer,
  "total":fields.Float
}


class getAllOrdersIdAdminApi(Resource):
  @level_required(2)
  @marshal_with(order_data)
  def get(current_user,self):
    try:
     
      
      orders = Order.query.group_by(Order.order_id, Order.order_date)\
        .add_columns(
          Order.order_id, Order.order_date, 
          db.func.count(Order.product_id).label('product_count'), 
          db.func.sum(Order.total).label('total'),
          )\
       .all()

      data = []
      
      for order in orders:
        order_date = order.order_date
        order_month = order_date.strftime("%B")
        order_year = order_date.strftime("%Y")
        data.append({
          "order_id":order.order_id,
          "order_date":order.order_date,
          "order_month":order_month,
          "order_year":order_year,
          "product_count":order.product_count,
          "total":order.total
        })
      
       
       
      
      if not orders:
        raise BusinessValidationError(400, "ORDER_NOT_FOUND", "Order not found")
      return data, 200
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))