import os 
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask,request,jsonify
from flask import url_for
from app.models import db as mongo_db 
from app.models import app_bcrypt
from app.views import app_jwt
from app.views import app_mail
from app.views.api import api_blueprint
from app.views.user import api_user_blueprint
from app.views.review import api_review_blueprint
from app.config import config 
from app.logger import logger

LOG = logger.get_root_logger(__name__)

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
    app_created = Flask(__name__)
    app_created.config.from_object(config[config_name])
    config[config_name].init_app(app_created)
    app_created.json_encoder = JSONEncoder
    
    ## Init Extensions 
    mongo_db.init_app(app_created)
    app_bcrypt.init_app(app_created)
    app_jwt.init_app(app_created)
    app_mail.init_app(app_created)
    
    ## Register API Blueprints 
    api_blueprint.register_blueprint(api_user_blueprint)
    api_blueprint.register_blueprint(api_review_blueprint)
    app_created.register_blueprint(api_blueprint)
    LOG.info('register endpoint in %s',app_created.url_map)

    ## Error Handlers 
    @app_created.errorhandler(404)
    @app_created.errorhandler(405)
    def _handle_api_error(ex):
        if request.path.startswith('/api/'):
            return jsonify({ 'ok':False, 'error':str(ex)}), ex.code
        else:
            return ex

    return app_created

if os.environ.get('APP_ENV') != 'production':
    application = create_app('DEV')
else:
    application = create_app('PRD')


