class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://flaskuser:flaskpassword@localhost/mechanic_shop_db'
    DEBUG = True
    SECRET_KEY = 'a-long-random-secret-string-change-this-later'

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'a-long-random-secret-string-change-this-later'
    CACHE_TYPE = 'SimpleCache'

import os

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-long-random-secret-string-change-this-later'
    CACHE_TYPE = "SimpleCache"
