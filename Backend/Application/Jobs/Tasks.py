
from celery import shared_task
from Application.models import *
from datetime import datetime, date
import flask_excel as excel
from json import dumps
from httplib2 import Http

import moment


@shared_task(ignore_result=False)
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
  pass



