from flask_restful import Resource, reqparse, fields, marshal_with
from flask import current_app as app,jsonify, make_response
from werkzeug.security import check_password_hash
from Application.models import User
from Application.db import db
from Application.error_handling import BusinessValidationError
from datetime import datetime, timedelta
import jwt



loginParser = reqparse.RequestParser()

loginParser.add_argument("email", type=str, required=True, help="Email or username is required")
loginParser.add_argument("password", type=str, required=True, help="Password is required")


class Login(Resource):
  

  def post(self):
    try:
      args = loginParser.parse_args()
      print(args)
      
      if args['email'] is None or args['password'] is None:
        print("Email and password are required")
        raise BusinessValidationError("Email and password are required")
      
      else:
        user = User.query.filter_by(email=args['email']).first()
        
        if user is None:
          print("User not found")
          raise BusinessValidationError(404,"USER404","User not found")
        
        else:
          if check_password_hash(user.password_hash, args['password']):
            print("User found")
            token = jwt.encode({'user': user.username, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
            print(token)
            user.jwt_token = token
            db.session.commit()
            return make_response(jsonify({'user': user.email, 'token': token}), 200)
          else:
            print("Incorrect password")
            raise BusinessValidationError(403,"USER403","Incorrect password")
          
    except BusinessValidationError as e:
      return make_response(jsonify({'error': str(e)}), 400)
      
      
      
      
    
    
   


