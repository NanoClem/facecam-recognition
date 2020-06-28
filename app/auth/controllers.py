from flask import flash, redirect

from ..extensions import flask_bcrypt
from ..api.users.controllers import User



# LOGIN CONTROLLER
class LoginController(object):

    @classmethod
    def check_password(cls, plain_psswd: str, hash_psswd: bytes) -> bool:
        """
        """
        return flask_bcrypt.check_password_hash(hash_psswd, plain_psswd)

    @classmethod
    def try_login(cls, email: str, password: str) -> bool:
        """
        """
        user = User.getByEmail(email)
        if user:
            return cls.check_password(password, user['password'])
        return False


# REGISTER CONTROLLER
class RegisterController(object):

    @classmethod
    def hash_password(cls, password: str) -> bytes:
        """
        """
        return flask_bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def register_user(cls, email, pseudo: str, password: str) -> bool:
        """
        """
        user = User.getByEmail(email)
        if not user:
            user_obj = User(email, pseudo, cls.hash_password(password))
            return True if User.create_user(user_obj.toJSON()) else False
        return False