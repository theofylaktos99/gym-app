"""
Custom decorators for the application
"""
from functools import wraps
from flask import session, request, abort, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User

def tenant_required(f):
    """Decorator to ensure tenant_id is present"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        tenant_id = request.headers.get('X-Tenant-ID') or session.get('tenant_id')
        if not tenant_id:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Tenant ID required'}), 400
            abort(400, 'Tenant ID required')
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to check user role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if using JWT or session
            if request.headers.get('Authorization'):
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.get(user_id)
            else:
                user_id = session.get('user_id')
                if not user_id:
                    abort(401, 'Authentication required')
                user = User.query.get(user_id)
            
            if not user or user.role not in roles:
                abort(403, 'Insufficient permissions')
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
