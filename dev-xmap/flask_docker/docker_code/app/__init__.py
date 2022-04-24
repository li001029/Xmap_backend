import os 
from flask import Flask
import logging 
from .config import config 

def create_app(config_name):
    """Create a new app instances"""
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger("flask").setLevel(logging.DEBUG)
    app_created = Flask(__name__)
    app_created.config.from_object(config[config_name])
    config[config_name].init_app(app_created)

    return app_created

if os.environ.get('APP_ENV') != 'production':
    application = create_app('DEV')
else:
    application = create_app('PRD')

