from flask_login import UserMixin
from db import *


# Simulate user database
USERS_DB = {}


class mxUser(UserMixin):

    """Custom User class."""

    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    def claims(self):
        """Use this method to render all assigned claims on profile page."""
        return {'name': self.name,
                'email': self.email}.items()

    @staticmethod
    def get(user_id):
        return USERS_DB.get(user_id)
        #aDb = get_database()     
        #if aDb.settings.find({'_id': aId}).count() <= 0:
        #return aDb.Users.settings.find({'_id': user_id})

    @staticmethod
    def create(user_id, name, email):
        USERS_DB[user_id] = mxUser(user_id, name, email)
            
        #aDb = get_database()
        #usr = mxUser(id_ = user_id, name = name, email = email)
        #usr.email = email
        #usr.name = name
        #aDb['Users'].settings.insert_one(usr)        
        #aDb.insert_one(usr)        
        #usr.save()
