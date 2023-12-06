from flask import current_app as app, jsonify, make_response
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from Application.models import User
from Application.db import db
from Application.error_handling import BusinessValidationError, TokenExpiredError, TokenInvalidError, InsufficientLevelError
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
        raise BusinessValidationError("Email and password are required")

      user = User.query.filter_by(email=args['email']).first()

      if not user:
        raise BusinessValidationError(404, "USER404", "User not found")

      if not check_password_hash(user.password_hash, args['password']):
        raise BusinessValidationError(403, "USER403", "Incorrect password")

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
      return make_response(jsonify({'success': False, 'error': str(e)}), 400)

    except TokenExpiredError as te:
      return make_response(jsonify({'success': False, 'error': 'Token has expired'}), 401)

    except TokenInvalidError as ti:
      return make_response(jsonify({'success': False, 'error': 'Token is invalid'}), 401)

    except InsufficientLevelError as ire:
      return make_response(jsonify({'success': False, 'error': 'Insufficient privileges'}), 403)

    except Exception as ex:
      # Log the exception for further debugging
      app.logger.error(f"Unexpected error in Login: {str(ex)}")
      return make_response(jsonify({'success': False, 'error': 'Internal Server Error'}), 500)


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
        raise BusinessValidationError(404, "USER404", "User not found")

    except BusinessValidationError as e:
      return make_response(jsonify({'success': False, 'error': str(e)}), 404)

    except Exception as ex:
      app.logger.error(f"Unexpected error in Logout: {str(ex)}")
      return make_response(jsonify({'success': False, 'error': 'Internal Server Error'}), 500)
