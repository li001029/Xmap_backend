from crypt import methods
from flask import (
    jsonify, request, Blueprint
)
from flask_jwt_extended import (
    jwt_required,create_access_token, get_current_user
)
from app.models.user import User 
from app.schema.user import validate_user_form,validate_reset_password_form
from app.views import app_jwt
from app.logger import logger
from app.utils import send_reset_password_link, is_valid_email

LOG = logger.get_root_logger(__name__)


api_user_blueprint = Blueprint('users',__name__,url_prefix='/users')

@api_user_blueprint.route('/',methods=['GET'])
def get_users():
    """User endpoint. return all registered users 

    list of users can be filter via `?page` and `?limit`. 

    Returns:
        list of app.models.user.User : all registered users in x-map
    """
    if request.method == 'GET':
        page = int(request.args.get('page',1))
        limit = int(request.args.get('limit',10))
        all_users = User.objects().order_by('create_at').only('email','first_name','last_name').paginate(page=page,per_page=limit)
        return jsonify({'ok':True, 'data': [user for user in all_users.items],'page_num':page, 'per_page':limit, 'total_results': len(all_users.items)}), 200

@api_user_blueprint.route('/register',methods=['POST'])
def register():
    """ Register new user by parsing a POST request containing user credentials 
    """
    LOG.debug(request.get_json())
    data = validate_user_form(request.get_json(force=True))
    if not data['ok']: 
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

    data = data['data'] 
    email = data['email']
    if not is_valid_email(email):
        return jsonify({'ok':False, 'message': 'Bad request parameters: Invalid email formatting '}), 400

    user_data = User.get_user_by_email(email=email)

    if user_data == None: 
        ## email is not registed 
        User.create(**data)
        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200 
    else:
        return jsonify({'ok':False, 'message': 'Bad request parameters: {}'.format('User already exists!')}), 400

@api_user_blueprint.route('/<email>',methods=['GET','DELETE','PUT'])
@jwt_required()
def current_user(email):
    if request.method == 'GET':
        pass 

    if request.method == 'DELETE':
        pass

    if request.method == 'PUT':
        pass 
