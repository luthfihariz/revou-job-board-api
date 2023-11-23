from core.user.constants import UserRole
import jwt, os
from flask import request, g
from functools import wraps

def decode_jwt(token):   
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        print("Expired signature error")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token error")
        return None
    

def admin_required(fn):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"error": "Token is not valid"}, 401
        
        try:
            decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms="HS256")
            user_id = decoded_token.get("user_id")
            user_role = decoded_token.get("role")
            if user_role == UserRole.ADMIN.value:
                return fn(user_id, *args, **kwargs)
            else:
                return {"error": "Admin access is required"}, 403
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Token is not valid"}, 401
    return wrapper


def job_seeker_required(fn):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"error": "Token is not valid"}, 401
        
        try:
            decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms="HS256")
            user_id = decoded_token.get("user_id")
            user_role = decoded_token.get("role")
            if user_role == UserRole.JOB_SEEKER.value:
                return fn(user_id, *args, **kwargs)
            else:
                return {"error": "Job seeker access is required"}, 403
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Token is not valid"}, 401
    return wrapper


def user_required(fn):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"error": "Token is not valid"}, 401
        
        try:
            decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms="HS256")
            user_id = decoded_token.get("user_id")
            if user_id:
                return fn(user_id, *args, **kwargs)
            else:
                return {"error": "User access is required"}, 403
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Token is not valid"}, 401
    return wrapper