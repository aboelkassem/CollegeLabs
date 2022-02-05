import os

class Config:
    DEBUG = False
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    SQLALCHEMY_DATABASE_URI = str(os.environ.get('DATABASE_URL'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
