from flask import Flask
from flask_cors import CORS
from config import LocalDevelopmentConfig
from Application.db import db
from Application import workers
from flask_restful import Api
import flask_excel as excel

import os



app = None
api = None
celery = None


def create_app():
  app = Flask(__name__, template_folder='templates', static_folder='static')
  
  CORS(app)
  
  
  if os.getenv('ENV', "development") == 'Production':
    raise Exception("Not available")
  else:
    print("Running in development mode")
    app.config.from_object(LocalDevelopmentConfig)

  db.init_app(app)
  api = Api(app)
  api.init_app(app)
  excel.init_excel(app)
  
  with app.app_context():  
    celery = workers.celery
    celery.conf.update(
      broker_url=app.config['CELERY_BROKER_URL'],
      result_backend=app.config['CELERY_RESULT_BACKEND'],
      result_expires=3600,
      enable_utc=False,
      timezone='Asia/Kolkata',
    )
    celery.Task = workers.ContextTask
  app.app_context().push()

  return app, api, celery

app, api, celery = create_app()


from Application.APIs.User.LoginLogoutSignUp import Login, Logout, SignUp
from Application.APIs.Category.Category import CategoryGeneralAPI, CategoryAdminAPI, CategoryByIdAPI,CategoryRequestAPI
from Application.APIs.Category.CategoryManager import CreateCategoryRequestByManagerAPI, UpdateCategoryRequestByManagerAPI, DeleteCategoryRequestByManagerAPI


# user apis
api.add_resource(Login, '/api/v1/user/login')
api.add_resource(Logout, '/api/v1/user/logout')
api.add_resource(SignUp, '/api/v1/user/signup')

# category apis
api.add_resource(CategoryGeneralAPI, '/api/v1/category/get/all')
api.add_resource(CategoryByIdAPI, '/api/v1/category/get/<int:category_id>')

# category admin apis
api.add_resource(CategoryAdminAPI, '/api/v1/category/admin/create')
api.add_resource(CategoryAdminAPI, '/api/v1/category/admin/update')
api.add_resource(CategoryAdminAPI, '/api/v1/category/admin/delete')

# category request apis
api.add_resource(CategoryRequestAPI, '/api/v1/category/request/get/all')
api.add_resource(CategoryRequestAPI, '/api/v1/category/request/approval')

# category manager apis
api.add_resource(CreateCategoryRequestByManagerAPI, '/api/v1/category/manager/create')
api.add_resource(UpdateCategoryRequestByManagerAPI, '/api/v1/category/manager/update')
api.add_resource(DeleteCategoryRequestByManagerAPI, '/api/v1/category/manager/delete')



if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)
  