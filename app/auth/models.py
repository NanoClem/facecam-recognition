from flask_login import UserMixin
import bcrypt

from ..extensions import login_manager



class User(UserMixin):
    """
    """

    def __init__(self, username):
      self.username = username


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


    @classmethod
    def getByEmail(cls, email):
        return {'email': email, 'password': b'$2b$12$zP/rp3o2zLuACt8TYd/FtOpSyDkKpNts4Te1Iu0RKs07xMR7tvMfu'}
    
