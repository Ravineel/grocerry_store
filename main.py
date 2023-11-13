from flask import Flask
from flask_restful import Api
from Application.config import LocalDevelopmentConfig
from Application.database import db
from Application import workers
from Application.Backend_Jobs.Task import task
import os

app = None
api = None
celery = None

def create_app():
  app = Flask(__name__, template_folder='templates', static_folder='static')
  
  if os.getenv('ENV', "development") == 'Production':
    raise Exception("Not available")
  else:
    print("Running in development mode")
    app.config.from_object(LocalDevelopmentConfig)

  db.init_app(app)
  api = Api(app)
  
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

    # if db/db.sqlite does not exist, create it
    if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')):
      db.create_all()
      print("Database created")
    else:
      print("Database already exists")


  return app, api, celery

app, api, celery = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
