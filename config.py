from dotenv import load_dotenv
import os
import redis
load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ['SECRET_KEY']
    MONGODB_SETTINGS = {
    'host': 'mongodb+srv://aashir:aashir123@cluster0.swovdoe.mongodb.net/?retryWrites=true&w=majority'
    }
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    UPLOAD_FOLDER = 'files'


