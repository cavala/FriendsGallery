from pymongo import MongoClient
import pymongo
from mongoengine import connect
import key_config as key


def get_database():    
    #client = MongoClient(CONNECTION_STRING, alias='myFirstDatabase')
    #db = client  
    db = connect(
        db= key.db_name,
        username=key.db_username,
        password=key.db_password,
        host= key.db_host
    )
    return db