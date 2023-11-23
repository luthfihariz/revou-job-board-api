from core.auth.ports import IHashingProvider
from infrastructure.auth.adapters import BcryptHashingProvider
from injector import Module, singleton, Binder

class AuthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IHashingProvider, to=BcryptHashingProvider, scope=singleton) 