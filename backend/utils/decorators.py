from functools import wraps
import inspect
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user:
                return jsonify({
                    "error": "User not found"
                }), 404
            if not user.is_active:
                return jsonify({
                    "error": "Account is deactivated"
                }), 403
            if user.is_blacklisted:
                return jsonify({
                    "error": "Account is blacklisted"
                }), 403
            if allowed_roles and user.role not in allowed_roles:
                return jsonify({
                    "error": "Access denied. Insufficient role."
                }), 403
            sig = inspect.signature(fn)
            if 'current_user_id' in sig.parameters:
                kwargs['current_user_id'] = user_id
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def validate_json(*required_fields):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent = True)

            if data is None:
                return jsonify({
                    "error": "Request body MUST be JSON"
                }), 400
            
            if not data:
                return jsonify({
                    "error": "Request body cannot be empty."
                }), 400
            
            missing = [f for f in required_fields if f not in data]
            if missing:
                return jsonify({
                    "error": f"Missing required fields: {', '.join(missing)}"
                }), 400
            kwargs['data'] = data
            return fn(*args, **kwargs)
        return wrapper
    return decorator