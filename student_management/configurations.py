import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

BASE_DIR=os.path.dirname(os.path.realpath(__file__))


UPLOAD_FOLDER = 'static/uploads'
class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY') 
    SQLALCHEMY_TRACK_MODIFICATIONS=True 
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(BASE_DIR, 'database.sqlite3' )
    UPLOAD_FOLDER = UPLOAD_FOLDER 
    # UPLOAD_FOLDER = os.path.join( BASE_DIR, 'media' )


class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS=False


config_dict = {
    'dev': DevelopmentConfig ,
    'pro' : ProductionConfig ,
    'test': TestingConfig
}