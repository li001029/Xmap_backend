import os 

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

    @staticmethod
    def init_app(app):
        pass


# SERVER_NAME enables URL generation without a request context but with an application context.
class DevConfig(BasicConfig):
    TESTING = True 

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

