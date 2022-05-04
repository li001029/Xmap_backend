import os 
import datetime

class BasicConfig(object):
    """Base config"""
    DEBUG = os.environ["APP_DEBUG"] == "true"
    TESTING = False 
    APP_ENV = os.environ["APP_ENV"]

    ## set Flask config 
    API_VERSION = "1.0"

    ## Set MongoDB config 
    DB_URI = os.environ["DB_URL"]
    MONGODB_HOST = DB_URI

    ## Set JWT config 
    JWT_SECRET_KEY = os.environ.get('SECRET')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)

    @staticmethod
    def init_app(app):
        pass


# SERVER_NAME enables URL generation without a request context but with an application context.
class DevConfig(BasicConfig):
    TESTING = True 
    MAIL_SUPPRESS_SEND = False # testing email 
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    

class PrdConfig(BasicConfig):
    TESTING = False
    
class TestConfig(BasicConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

    MONGODB_SETTINGS = {
        'DB': 'Test',
        'IS_MOCK': True
    }

config = {
    'DEV': DevConfig,
    'PRD': PrdConfig,
    'TEST': TestConfig,
    'DEFAULT': DevConfig,
}

