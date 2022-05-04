from crypt import methods
from flask import (Blueprint , request, jsonify)
from flask_jwt_extended import create_access_token, jwt_required, get_current_user
from app.schema.user import validate_reset_password_form, validate_user_form
from app.models.user import User
from app.logger import logger
from app.utils import is_valid_email, send_reset_password_link

LOG = logger.get_root_logger(__name__)

api_blueprint = Blueprint('api',__name__,url_prefix='/api')

@api_blueprint.route('/',methods=['GET',])
def home():
    return jsonify({"ok":True,'message': "Welcome to x-map api"}), 200

@api_blueprint.route('/login',methods=['POST',])
def login():
    """
    Authenticate a user in by parsing a POST request containing user credentials and
    return a JWT token.

    .. example::
       $ curl http://localhost:5001/api/login -X POST \
         -d '{"email":"test@example.com","password":"strongpassword"}'
    """
    data = validate_user_form(request.get_json())
    if not data['ok']: 
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400
    
    data = data['data'] 
    email = data['email']
    if not is_valid_email(email):
        return jsonify({'ok':False, 'message': 'Invalid email address provided '}), 400

    user_data = User.get_user_by_email(email=email)
    if (user_data and user_data.validate_user(data['password'])):
        del user_data.password
        access_token = create_access_token(identity=user_data)
        return jsonify({'ok': True, 'access_token': access_token}), 200
    else:
        return jsonify({'ok': False, 'message': 'invalid username or password'}), 401

@api_blueprint.route('/protected',methods=['GET',])
@jwt_required()
def protected():
    """
    A protected endpoint. The jwt_required decorator will require a header
    containing a valid JWT, which will kick out requests without a valid JWT present. 
    This will return current user as data
    .. example::
       $ curl http://localhost:5001/api/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    current_user = get_current_user()
    del current_user.password 
    return jsonify({'ok': True, 'data':current_user, 'message':  f'protected endpoint (allowed user {current_user.id})'}), 200

@api_blueprint.route('/reset',methods=['POST'])
def reset_password():
    """ Reset user password by parsing a POST request containing user emails, old password and new pasword 
    """
    data = validate_reset_password_form(request.get_json(force=True))
    if not data['ok']: 
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400
    
    data = data['data']
    email = data['email']
    if not is_valid_email(email):
        return jsonify({'ok':False, 'message': 'Invalid email address provided '}), 400

    user_data = User.get_user_by_email(email=email)
    if user_data is None:
        return jsonify({'ok':False,'message':'User not found'}), 404 
    
    access_token = create_access_token(identity=user_data)
    try:
        send_reset_password_link(user_data,access_token)

        return jsonify({"ok":True, 'message':"Password reset email has been sent"}), 200
    except Exception as e:
        LOG.error(e) 
        
        return jsonify({'ok':False, 'message':'There was a problem sending the password set email. Please try again later'}), 500


@api_blueprint.route('/logout',methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'ok':True, 'message':"logout successful"})