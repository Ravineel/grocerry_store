
from celery import shared_task
from Application.models import *
from datetime import datetime, date
import flask_excel as excel
from json import dumps
from httplib2 import Http
from Application.Jobs.reportMaker import create_report
from Application.Jobs.sendMail import sendMail
import os
import moment


@shared_task(ignore_result=True)
def send_user_alert():
  try:
   
    users  = User.query.filter_by(role=1).all()
    
    msg =""
    url ="https://chat.googleapis.com/v1/spaces/AAAAcxz7wDE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=mWsmcfkK8pIzDCIfCFmDhQRs5eHXEBBKRO97P3F657k"
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    
    if users:
      for user in users:

        if user.last_login is None:
          msg = "Hi {}, you have not visited the site today, please visit to get the latest Products".format(user.first_name + " " + user.last_name)
        
        elif user.last_login.date() != date.today():
          msg = "Hi {}, you have not visited the site today, please visit to get the latest Products".format(user.first_name + " " + user.last_name)
      
        else:
          if not user.orders:
            msg = "Hi {}, you have not made any purchase yet, please head to the site to get the latest Products".format(user.first_name + " " + user.last_name)
          elif user.orders[-1].order_date.date() != date.today():
            msg = "Hi {}, you have not made any purchase today, please head to the site to get the latest Products".format(user.first_name + " " + user.last_name)
        
        response = http_obj.request(
          uri=url,
          method="POST",
          headers=message_headers,
          body=dumps({"text": msg})
        )  
       
  except Exception as e:
    print(e)
    raise e
    


@shared_task(ignore_result=False)
def send_user_email():
  users  = User.query.filter_by(role=1).all()
  current_month = datetime.now().month
  current_year  = datetime.now().year
  message_type = "pdf" #or html
  response = None
  
  if users:
    for user in users:
      # get the orders of the user for the current month and year
      
      if user.orders:
      
        orders = user.orders
        orders = [order for order in orders if order.order_date.month == current_month and order.order_date.year == current_year]
      
        total_orders = len(orders)
        total_expense = 0
        
        # product_ids and coounts
        frequency = {}
        frequent_product_id = None
        
        most_bought_product_id = None
        product_bought = {}
        
        for order in orders:
          total_expense += order.total
          frequency[order.product_id] = frequency.get(order.product_id, 0) + 1
          product_bought[order.product_id] = product_bought.get(order.product_id, 0) + order.qty
        
        for key, value in frequency.items():
          if frequent_product_id is None:
            frequent_product_id = key
          elif frequency[frequent_product_id] < value:
            frequent_product_id = key
            
        for key, value in product_bought.items():
          if most_bought_product_id is None:
            most_bought_product_id = key
          elif product_bought[most_bought_product_id] < value:
            most_bought_product_id = key
        
              
        frequent_product = Product.query.filter_by(product_id=frequent_product_id).first()
        most_bought_product = Product.query.filter_by(product_id=most_bought_product_id).first()
        
      
        #send mail
      
        products = Product.query.all()
    
        reponse = create_report(
          user, 
          total_orders, 
          total_expense, 
          frequent_product,
          frequency[frequent_product_id], 
          most_bought_product,
          product_bought[most_bought_product_id], 
          message_type
        )
        
        print(reponse)
        
      else:
        message_type="text"
        
        
        
      if message_type == "html":
        sendMail(user.email, message_type, html_message=reponse["html_message"])
      elif message_type == "pdf":
        sendMail(user.email, message_type, file_name=reponse["file_name"])
      else:
        sendMail(user.email, message_type=message_type)
        
      

@shared_task(ignore_result=False)
def product_excel():
  try:
    
    # Get product deatils + from order get prodcut qty sold and total amount
    
    orders = db.session.query(
            Order.product_id,
            db.func.count().label('product_bought_count'),
            db.func.sum(Order.total).label('product_total_revenue'),
            db.func.sum(Order.qty).label('product_sold')
        ).group_by(Order.product_id).subquery()

    product_report = db.session.query(
            Product.product_id,
            Product.product_name,
            Product.description,
            Product.rate,
            Product.unit,
            Product.qty.label('product_available_qty'),
            orders.c.product_bought_count,
            orders.c.product_total_revenue,
            orders.c.product_sold
        ).outerjoin(orders, Product.product_id == orders.c.product_id).all()
      
    print(product_report)
    
    filename = "product_report.csv"
    csv_output = excel.make_response_from_query_sets(product_report, ["product_id", "product_name", "description", "rate", "unit", "product_available_qty", "product_bought_count", "product_total_revenue", "product_sold"], "csv")
  
    with open(filename, "wb") as f:
      f.write(csv_output.data)   
 
    return filename
 
  except Exception as e:
    raise e
    
      
      
      