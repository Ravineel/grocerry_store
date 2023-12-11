from Application.workers import celery
from celery.schedules import crontab
from Application.models import *
from datetime import datetime
import flask_excel as excel
from json import dumps
from httplib2 import Http


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    crontab(minute=2, hour="*", day_of_week='*'),
    send_user_alert.s(),
    name='send_user_alert'
  )  
  sender.add_periodic_task(
    crontab(minute=0, hour=0, day_of_month=1, month_of_year='*'),
    send_user_email.s(),
    name='send_user_email'
  )
  

@celery.task()
def send_user_alert():
  try:
   
    users  = User.query.filter_by(role=1).all()
    
    msg =""
    url ="https://chat.googleapis.com/v1/spaces/AAAAcxz7wDE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=mWsmcfkK8pIzDCIfCFmDhQRs5eHXEBBKRO97P3F657k"
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    
    if users:
      for user in users:
        if user.last_login != datetime.date.today():
          msg = "Hi {}, you have not visited the site today, please visit to get the latest Products".format(user.first_name + " " + user.last_name)
        else:
          if not user.orders:
            msg = "Hi {}, you have not made any purchase yet, please make one to get the latest Products".format(user.first_name + " " + user.last_name)
          elif user.orders[-1].order_date != datetime.date.today():
            msg = "Hi {}, you have not made any purchase today, please make one to get the latest Products".format(user.first_name + " " + user.last_name)
        
        response = http_obj.request(
          uri=url,
          method="POST",
          headers=message_headers,
          body=dumps({"text": msg})
        )  
        print(response)
  except Exception as e:
    print(e)
    raise e
    


@celery.task()
def send_user_email():
  pass



