from core.auth.ports import IHashingProvider
from core.user.constants import UserRole
from core.user.ports import IUserAccessor
from core.user.models import UserDomain
from injector import inject
import jwt, os
from datetime import datetime, timedelta

class AuthService():

    @inject
    def __init__(self, user_accessor: IUserAccessor, hashing_provider: IHashingProvider) -> None:
        self.user_accessor = user_accessor
        self.hashing_provider = hashing_provider

    def register(self, username: str, password: str, email:str, role: UserRole) -> UserDomain:
        hashed_password = self.hashing_provider.generate(password)
        user = self.user_accessor.create_user(
            username,
            hashed_password,
            email,
            role
        )   
        return user

    def login(self, username: str, password: str):
        user = self.user_accessor.get_by_username(
            username
        )

        if not user:
            return None
        
        valid = self.hashing_provider.check_hash(user.password, password)

        if not valid:
            return None
        
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
            'exp': datetime.utcnow() + timedelta(minutes=10)
        }, os.getenv('SECRET_KEY'), algorithm='HS256')    
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token
        }