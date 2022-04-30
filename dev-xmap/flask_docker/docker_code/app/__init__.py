import os 
import json
import datetime
import logging 
from bson.objectid import ObjectId
from flask import Flask
from flask_bcrypt import Bcrypt
# Set up extensiosn 
from app.models import db as mongo_db 
from app.config import config 

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

def create_app(config_name):
    """Create a new app instances"""
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger("flask").setLevel(logging.DEBUG)
    app_created = Flask(__name__)
    app_created.config.from_object(config[config_name])
    config[config_name].init_app(app_created)
    app_created.json_encoder = JSONEncoder
    ## Init Extensions 
    mongo_db.init_app(app_created)

    return app_created

if os.environ.get('APP_ENV') != 'production':
    application = create_app('DEV')
else:
    application = create_app('PRD')

bcrypt = Bcrypt(application)