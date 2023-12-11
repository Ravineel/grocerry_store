from flask import Flask
from flask_cors import CORS
from config import LocalDevelopmentConfig
from Application.db import db
from Application.workers import celery_init_app
from Application.Jobs.Tasks import send_user_alert, send_user_email
from flask_restful import Api
import flask_excel as excel
from celery.schedules import crontab


import os



app = None
api = None

def create_app():
  app = Flask(__name__, template_folder='Template', static_folder='static')
  
  CORS(app)
  app.config.from_object(LocalDevelopmentConfig)

  db.init_app(app)
  api = Api(app)
  api.init_app(app)
  excel.init_excel(app)
  app.app_context().push()
  app.config.from_mapping(
    CELERY=dict(
      broker_url = "redis://localhost:6379/1",
      result_backend = "redis://localhost:6379/2",
      enable_utc = False,
      timezone = 'Asia/Kolkata',
      broker_connection_retry_on_startup=True
    ),
  )

  return app, api
app, api = create_app()


celery_app = celery_init_app(app)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    crontab(minute='*', hour="*", day_of_week='*'),
    send_user_alert.s(),
    name='send_user_alert'
  )  
  sender.add_periodic_task(
    crontab(minute=30, hour=17, day_of_month=1, month_of_year='*'),
    send_user_email.s(),
    name='send_user_email'
  )
 




from Application.APIs.User.LoginLogoutSignUp import Login, Logout, SignUp
from Application.APIs.User.User import userManagerRole, userCount
from Application.APIs.Category.Category import CategoryGeneralAPI, CategoryAdminAPI, CategoryByIdAPI,CategoryRequestAPI
from Application.APIs.Category.CategoryManager import RequestCategoryRequestByManagerAPI
from Application.APIs.Product.Product import ProductGeneralAPI, ProductByIdAPI, ProductManagerAPI
from Application.APIs.Order.Order import CheckoutApi, getAllOrdersIdUserApi, getUserOrdersApi, getAllOrdersIdAdminApi


# user apis
api.add_resource(Login, '/api/v1/user/login')
api.add_resource(Logout, '/api/v1/user/logout')
api.add_resource(SignUp, '/api/v1/user/signup')


# user manager apis
api.add_resource(userManagerRole, '/api/v1/admin/get/manager','/api/v1/admin/update/manager')

# user count apis
api.add_resource(userCount, '/api/v1/admin/get/user_count')

# category apis
api.add_resource(CategoryGeneralAPI, '/api/v1/category/get/all')
api.add_resource(CategoryByIdAPI, '/api/v1/category/get/<int:category_id>')

# category admin apis
api.add_resource(CategoryAdminAPI, '/api/v1/category/admin/create','/api/v1/category/admin/update','/api/v1/category/admin/delete')


# category request apis
api.add_resource(CategoryRequestAPI, '/api/v1/category/request/get/all','/api/v1/category/request/approval')


# category manager apis
api.add_resource(RequestCategoryRequestByManagerAPI, '/api/v1/category/manager/request/create','/api/v1/category/manager/request/get')

# product apis
api.add_resource(ProductGeneralAPI, '/api/v1/product/get/all')

# product manager apis
api.add_resource(ProductManagerAPI, '/api/v1/product/create','/api/v1/product/update','/api/v1/product/delete')


# product by id apis
api.add_resource(ProductByIdAPI, '/api/v1/product/get/<int:product_id>')

#checkout api
api.add_resource(CheckoutApi, '/api/v1/order/checkout')

# get all orders id user api
api.add_resource(getAllOrdersIdUserApi, '/api/v1/user/orders/get/all')

# get user orders api
api.add_resource(getUserOrdersApi, '/api/v1/user/orders/get/orders_detail')

# get all orders id admin api
api.add_resource(getAllOrdersIdAdminApi, '/api/v1/admin/orders/get/all')



if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)
  