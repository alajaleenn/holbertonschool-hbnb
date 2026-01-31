"""
Custom decorators for authorization.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.services import shared_facade


def admin_required():
    """Require admin privileges."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = shared_facade.get_user(user_id)
                
                if not user:
                    return jsonify({'error': 'User not found'}), 404
                
                if not user.is_admin:
                    return jsonify({'error': 'Admin privileges required'}), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Authorization failed'}), 401
        return decorator
    return wrapper
