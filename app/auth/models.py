from datetime import datetime
from flask_login import UserMixin
import bcrypt

from ..extensions import login_manager, mongo



class User(UserMixin):
    """
    """

    def __init__(self, email, pseudo, hash_password):
      self.email    = email
      self.pseudo   = pseudo
      self.password = hash_password


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    
    def toJSON(self):
        return {
            'email': self.email,
            'pseudo': self.pseudo,
            'password': self.password,
            'created_at': datetime.now()
        }

    @classmethod
    def getByEmail(cls, email):
        user = mongo.db.users.find_one({'email': email})
        if user:
            return {'email': user['email'], 'pseudo': user['pseudo'], 'password': user['password']}

    @classmethod
    def getByPseudo(cls, pseudo):
        user = mongo.db.users.find_one({'pseudo': pseudo})
        if user:
            return {'email': user['email'], 'pseudo': user['pseudo'], 'password': user['password']}

    @classmethod
    def save_user(cls, email, pseudo, hash_password) -> None:
        new_user = cls(email, pseudo, hash_password)
        mongo.db.users.insert_one(new_user.toJSON())
    
