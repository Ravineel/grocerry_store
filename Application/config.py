from datetime import timedelta
import os


class Config():
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
  DEBUG=False
  SQLITE_DB_DIR=None
  SQLALCHEMY_DATABASE_URI = None
  CELERY_BROKER_URL = 'redis://localhost:6379/1'
  CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

class LocalDevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/db.sqlite3'
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
  CELERY_BROKER_URL = 'redis://localhost:6379/1'
  CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

class SMTPConfig():
  SMPTP_SERVER_HOST = "localhost"
  SMPTP_SERVER_PORT = 1025
  SENDER_ADDRESS="mail@ravineel.com"
  SENDER_PASSWORD=""