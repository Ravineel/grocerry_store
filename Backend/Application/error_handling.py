from werkzeug.exceptions import HTTPException
from flask import make_response, jsonify

class CustomException(HTTPException):
	def __init__(self, status_code, error_code, error_message):
		data = {"error_code": error_code, "error_message": error_message}
		self.response = make_response(jsonify(data), status_code)

class TokenExpiredError(CustomException):
	def __init__(self):
		super().__init__(401, "TOKEN_EXPIRED", "Token has expired!")

class TokenInvalidError(CustomException):
	def __init__(self, error_message="Token is invalid!"):
		super().__init__(401, "TOKEN_INVALID", error_message)


class InsufficientLevelError(CustomException):
	def __init__(self):
		super().__init__(403, "INVALID_ROLE", "Insufficient privileges!")

class ValidationError(CustomException):
	def __init__(self, status_code, error_code, error_message):
		super().__init__(status_code, error_code, error_message)

class BusinessValidationError(CustomException):
	def __init__(self, status_code, error_code, error_message):
		super().__init__(status_code, error_code, error_message)

class NotFoundError(CustomException):
	def __init__(self, status_code, error_code, error_message):
		super().__init__(status_code, error_code, error_message)
