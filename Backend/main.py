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


from Application.APIs.User.LoginLogoutSignUp import Login, Logout

api.add_resource(Login, '/api/v1/login')
api.add_resource(Logout, '/api/v1/logout')

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)
  