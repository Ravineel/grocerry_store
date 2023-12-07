from flask import current_app as app, jsonify, make_response
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from Application.models import User
from Application.db import db
from Application.error_handling import BusinessValidationError
from Application.middleware import level_required
from datetime import datetime, timedelta
import jwt

login_parser = reqparse.RequestParser()
login_parser.add_argument("email", type=str, required=True, help="Email is required")
login_parser.add_argument("password", type=str, required=True, help="Password is required")

class Login(Resource):
  def post(self):
    try:
      args = login_parser.parse_args()

      if not args['email'] or not args['password']:
        raise BusinessValidationError(404, "MISSING_REQUIRED_PARAMETERS", "Email and password are required")
       

      user = User.query.filter_by(email=args['email']).first()

      if not user:
        raise BusinessValidationError(404, "USER_NOT_FOUND", "User not found")      

      if not check_password_hash(user.password_hash, args['password']):
        raise BusinessValidationError(403, "INVALID_PASSWORD_USERNAME", "Invalid password or USERNAME")

      # Generate JWT token with user information
      token = jwt.encode({
          'role': user.role,
          'email': user.email,
          'user_id': user.id,
          'exp': datetime.utcnow() + timedelta(minutes=30)
      }, app.config['SECRET_KEY'])

      user.jwt_token = token
      db.session.commit()

      response_data = {
          'success': True,
          'user': {
              'email': user.email,
              'role': user.role,
              'user_id': user.id,
              'user_name': f"{user.first_name} {user.last_name}"
          },
          'token': token
      }

      return make_response(jsonify(response_data), 200)
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    



logout_parser = reqparse.RequestParser()
logout_parser.add_argument("user_id", type=int, required=True, help="User ID is required")

class Logout(Resource):
  @level_required(minimum_level=1)
  def post(current_user,self ):  
    try:
      args = logout_parser.parse_args()
      user = User.query.filter_by(id=args['user_id']).first()
      
      if user:
        # Access current_user here
        print(f"Logging out user: {current_user.email}")

        user.jwt_token = None
        db.session.commit()
        
        return make_response(jsonify({'success': True, 'message': 'Successfully logged out'}), 200)
      else:
        raise BusinessValidationError(400, "USER_NOT_FOUND", "User not found")
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    
        


SingUp_parser = reqparse.RequestParser()
SingUp_parser.add_argument("username", type=str, required=True, help="Username is required")
SingUp_parser.add_argument("email", type=str, required=True, help="Email is required")
SingUp_parser.add_argument("password", type=str, required=True, help="Password is required") 
SingUp_parser.add_argument("first_name", type=str, required=True, help="First Name is required")
SingUp_parser.add_argument("last_name", type=str, required=False, help="Last Name is required")
SingUp_parser.add_argument("role", type=str, required=True, help="Role is required")

class SignUp(Resource):
  
  def post(self):
    try:
      args = SingUp_parser.parse_args()
      print(args)
      
      if not args['username'] or not args['email'] or not args['password'] or not args['first_name'] or not args['role']:
        raise BusinessValidationError(400, "MISSING_REQUIRED_PARAMETERS", "Username, email, password, first_name and role are required")
      
      user = User.query.filter_by(email=args['email']).first()
      
      if user:
        raise BusinessValidationError(400, "USER_ALREADY_EXISTS", "User already exists")
        
      
      if args['role'] == 'manager':
        role = 2
      else:
        role = 1
      
      new_user = User(
        username=args['username'],
        email=args['email'],
        password=args['password'],
        first_name=args['first_name'],
        last_name=args['last_name'],
        role=role,
        account_created_at=datetime.now()
      )
    
      db.session.add(new_user)
      db.session.commit()
      
      return make_response(jsonify({'success': True, 'message': 'Successfully signed up'}), 200)
    except BusinessValidationError as e:
      raise BusinessValidationError(e.status_code, e.error_code, e.error_message)
    except Exception as e:
      raise BusinessValidationError(500, "INTERNAL_SERVER_ERROR", str(e))
    
    