from infrastructure.auth.modules import AuthModule
from infrastructure.job.modules import JobModule
from injector import Injector
from infrastructure.user.modules import UserModule

injector = Injector([
    UserModule,
    JobModule,
    AuthModule,
])