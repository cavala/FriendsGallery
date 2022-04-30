from flask_mongoengine import MongoEngine
from mongoengine import *
from db import *

class User(Document):
    _id = StringField(required=True)
    email = StringField()
    name = StringField(max_length=100)

    #meta = {'allow_inheritance': True}


    def claims(self):
        """Use this method to render all assigned claims on profile page."""
        return {'name': self.name,
                'email': self.email}.items()

    @staticmethod
    def get(_id):
        aDb = get_database()        
        return aDb.User.settings.find_one({'_id': _id})
        

    @staticmethod
    def create(_id, email, name):        
        aDb = get_database()
        usr = User(_id= _id)
        usr.email = email
        usr.name = name            
        usr.save()
        

#class BrideAndGroom(User):
    