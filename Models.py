from flask_mongoengine import MongoEngine
from uuid import uuid4
from datetime import datetime

db = MongoEngine()



class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.now)
    
    meta = {'collection': 'Users'}
    
    def __str__(self):
        return self.username

class File(db.Document):
    filename = db.StringField(required=True)
    data = db.FileField(required=True)
    meta = {'collection': 'File'}