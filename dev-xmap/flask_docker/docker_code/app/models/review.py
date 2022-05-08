from datetime import datetime
import mongoengine
from app.models import db 
from app.models.user import User
from app.logger import logger

LOG = logger.get_root_logger(__name__)

class Review(db.Document):
    author = db.ReferenceField(User,reverse_delete_rule= mongoengine.CASCADE,required=True)
    park = db.IntField(required=True)
    rating = db.IntField(required=True)
    activity_date = db.DateTimeField(required=True)
    activity_type = db.StringField(default="")
    tags = db.ListField(db.StringField(max_length=30), default=list)
    comment = db.StringField(default="")
    created_at = db.DateTimeField(required=True,default=datetime.now())

    @classmethod
    def get_reviews_by_park(cls,park_id):
        """ Get user object by email given 

        Args:
            park_id (integer) : a particular park id 

        Returns: 
            (app.models.review.Review) : list of reviews created under a particular park 
        """

        return cls.objects(park_id=park_id).all()

    @classmethod
    def create(cls,save=True,**kwargs):
        """Create a new review based on requested data 

        Args:
            save (bool, optional):
                Whether or not to save the field 

                If ``False``, the caller is responsible for performing the
                save.
            
            **kwargs (dict):
                Keyword arguments representing additional fields handled by
                the API resource. Any that are also listed in ``fields`` will
                be set on the model.

        Returns:
            app.models.review.Review : new review just created
        """
        review_kwargs = {
            'author': kwargs.get('user'),
            'rating': kwargs.get('rating'),
            'park': kwargs.get('park_id'),
            'activity_date': datetime.strptime(kwargs.get('activity_date'), '%Y-%m-%d') 
        }
        fields = ['activity_type','tags','comment']
        for field in fields:
            review_kwargs[field] = kwargs.get(field,None) 
        
        new_review = Review(**review_kwargs)

        if save:
            new_review.save() 

        return new_review 





