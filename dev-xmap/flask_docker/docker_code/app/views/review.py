from bson import ObjectId
from flask import (
    jsonify, request, Blueprint
)
from flask_jwt_extended import (
    jwt_required, get_current_user
)
from app.models.user import User 
from app.models.review import Review
from app.schema.review import validate_review
from app.logger import logger
from app.utils import is_valid_email

LOG = logger.get_root_logger(__name__)


api_review_blueprint = Blueprint('reviews',__name__,url_prefix='/reviews')


@api_review_blueprint.route('/<park_id>',methods=['GET'])
def get_reviews_by_park(park_id):
    """Endpoint read reviews 
    list can be filtered by requested user only and activity_type via `?email` or `?activity_type`
    list of users can be filter via `?page` and `?limit`. 
    """
    if request.method == 'GET':
        reviews = Review.objects(park=park_id)
        filters = request.args
        if filters.get('email') is not None and is_valid_email(filters.get('email')):
            email = filters.get('email')
            user = User.get_user_by_email(email) 
            if user is not None:
                reviews.objects(author=user)

        if filters.get('activity_type') is not None:
            reviews.objects(activity_type=filters.get('activity_type'))

        page = int(request.args.get('page',1))
        limit = int(request.args.get('limit',10))
        reviews = Review.objects().order_by('activity_date').paginate(page=page,per_page=limit)
        
        data = list() 
        # TODO: anonymous posts
        for review in reviews.items:
            review.author = review.author.first_name + " " + review.author.last_name
            data.append(review.to_mongo())

        return jsonify({'ok':True, 'data': data,'page_num':page, 'per_page':limit, 'total_results': len(data)}), 200

@api_review_blueprint.route('',methods=['GET','POST','DELETE'])
@jwt_required()
def review():
    """
        review endpoint for requested user 
    """
    current_user = get_current_user()
    if request.method == 'GET':
        reviews = Review.objects(author=current_user).all()
        
        data = list() 
        for review in reviews:
            data.append(review.to_mongo())

        page = int(request.args.get('page',1))
        limit = int(request.args.get('limit',10))
        return jsonify({'ok':True, 'data': data,'page_num':page, 'per_page':limit, 'total_results': len(data)}), 200

    data = request.get_json(force=True)
    if request.method == 'DELETE':
        if data.get('id', None) is not None:
            review = Review.objects(id=ObjectId(data['id']))
            review_delete_count = review.delete()
            if review_delete_count == 0:
                return jsonify({'ok':False, 'message':"404 Not Found: The requested id was not found on the server. If you entered the id manually please check your spelling and try again."}), 404 
            else:
                return jsonify({'ok':True, 'message': 'review deleted successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: missing id field'}), 400

    data = validate_review(request.get_json(force=True))
    if request.method == 'POST':
        if not data['ok']: 
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400
        
        data = data['data']
        data['user'] = current_user
        new_review = Review.create(**data) 
        return jsonify({'ok':True, 'data': new_review.to_mongo(), 'message': 'Review created successfully!'}), 200 

