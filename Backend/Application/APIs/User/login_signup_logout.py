from flask_restful import Resource, reqparse
from flask import current_app as app,jsonify
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash, generate_password_hash
from Application.models import User, Role
from Application.database import db
from Application.security import datastore




loginParser = reqparse.RequestParser()

loginParser.add_argument("email", type=str, required=True, help="Email or username is required")
loginParser.add_argument("password", type=str, required=True, help="Password is required")


class Login(Resource):
  def post(self):
    try:
      print("Login")
      args = loginParser.parse_args()
      user = datastore.find_user(email = args["email"])
      
      
      if not user:
        print("User not found")
        return jsonify({"message": "Incorrect password or username","code":"USER404"}), 404
      
      if not user.active:
        print("User is not active")
        return jsonify({"message": "User is not active","code":"USER402"}), 403
      
      if check_password_hash(user.password_hash, args["password"]):
        print("Password matched")
      
        return jsonify({"tokem":user.get_auth_token(),"email": user.email, "role": user.roles[0].name})
      
      else:
        print("Password not matched")
        return jsonify({"message": "Incorrect password or username","code":"USER401"}), 401
      
    except Exception as e:
      return jsonify({"message": str(e),"code":"USER500"}), 500



signupParser = reqparse.RequestParser()
signupParser.add_argument("email", type=str, required=True, help="Email is required")
signupParser.add_argument("username", type=str, required=True, help="Username is required")
signupParser.add_argument("password", type=str, required=True, help="Password is required")
signupParser.add_argument("first_name", type=str, required=True, help="First name is required")
signupParser.add_argument("last_name", type=str, required=True, help="Last name is required")





class Signup(Resource):
  def post(self):
    try:
      args = signupParser.parse_args()
      if not datastore.find_user(email=args["email"]):
        return jsonify({"message": "User already exists","code":"USER409"}), 403
      else:
        datastore.create_user(
          email=args["email"],
          username=args["username"],
          first_name=args["first_name"],
          last_name=args["last_name"],
          password_hash=generate_password_hash(args["password"]),
          roles=["user"]
        )
        db.session.commit()
        return jsonify({"message": "User created successfully","code":"Success"}), 200
    except Exception as e:
      return jsonify({"message": str(e),"code":"USER500"}), 500
  
  
  