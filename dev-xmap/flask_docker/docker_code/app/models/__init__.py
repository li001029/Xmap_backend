from flask import current_app
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine 

db = MongoEngine()
app_bcrypt = Bcrypt()
