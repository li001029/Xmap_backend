from app.models import db 
from app import bcrypt
from datetime import datetime

class User(db.Document):
    email = db.StringField(required=True,primary_key=True)
    password = db.StringField(required=True) 
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    created_at = db.DateTimeField(required=True,default=datetime.now())

    @classmethod
    def get_user_by_email(cls,email):
        """ Get user object by email given 

        Args:
            email (str) : user email 

        Returns: 
            (app.models.user.User) : user object with the given email 
        """

        return cls.objects(email=email).first() 

    def validate_user(self,pwd):
        """ Validate password for the current user object 

        Args:
            pwd (str) : unhashed password 

        Returns:
            Bool: true if the password is correct, false otherwise
        """
        return bcrypt.check_password_hash(self.password,pwd)  

        

