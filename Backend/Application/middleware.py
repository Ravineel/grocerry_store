import jwt
from functools import wraps
from flask import current_app as app, request, jsonify
from Application.models import User
from Application.error_handling import ValidationError, TokenExpiredError, TokenInvalidError, InsufficientLevelError
import moment

# level 0 -> guest
# level 1 -> user
# level 2 -> admin

def level_required(minimum_level):
  def decorator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      token = None
      auth_header = request.headers.get('Authorization')

      if not auth_header:
        raise ValidationError(401, "TK002", "Token is missing")

      try:
        token = auth_header.split(" ")[1]
      except IndexError:
        raise ValidationError(401, "TK001", "Malformed token")

      try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_level = data.get('role', 0)
        
        current_user = User.query.filter_by(id=data['user_id']).first()
        
        if not current_user:
          raise ValidationError(401, "TK003", "User not found")

        if current_user.jwt_token != token:
          raise TokenInvalidError()
        
        if moment.unix(data["exp"]) < moment.now():
          raise TokenExpiredError()

        if user_level < minimum_level:
          raise InsufficientLevelError()

      
      except InsufficientLevelError as ile:
        raise ValidationError(403, "TK006", str(ile))
      except jwt.InvalidTokenError:
        raise TokenInvalidError()
      except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
      except Exception as e:
        raise ValidationError(401, "TK005", f"Token error: {str(e)}")

      return f(current_user, *args, **kwargs)

    return decorated

  return decorator
