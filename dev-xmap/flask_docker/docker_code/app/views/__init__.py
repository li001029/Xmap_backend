''' all controllers for various collections of database '''
from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from app.models.user import User


app_jwt = JWTManager()
app_mail = Mail() 

@app_jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
# for example get_jwt_identity() will return user email 
@app_jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
# this is get_current_user()
@app_jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.objects(email=identity).first()