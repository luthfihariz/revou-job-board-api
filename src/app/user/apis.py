from flask import Blueprint, request 
from app.auth.utils import decode_jwt, user_required
from core.user.services import UserService
from app.di import injector

user_service = injector.get(UserService)

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("", methods=["GET"])
@user_required
def get_user(user_id):
    user = user_service.get_by_id(user_id=user_id)
    if not user:
        return {"error": "User not found"}, 404
    
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }
    

