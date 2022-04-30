from email.policy import default
from tokenize import Number
from flask_mongoengine import MongoEngine
from mongoengine import *

from user import User

class Comment(EmbeddedDocument):    
    content = StringField(max_length=256)
    author = ReferenceField(User)

class Post(Document):    
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    likes = ListField(ReferenceField(User, reverse_delete_rule=DO_NOTHING))

    comments = ListField(EmbeddedDocumentField(Comment))
    meta = {'allow_inheritance': True}
    

#class TextPost(Post):    
#    content = StringField()

class ImagePost(Post):    
    imagename = StringField()
    visible = BooleanField(default = False)

