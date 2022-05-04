import os 
from datetime import datetime
from app.models import db 
from app.models import app_bcrypt



class User(db.Document):
    email = db.StringField(required=True,primary_key=True)
    password = db.StringField(required=True) 
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    created_at = db.DateTimeField(required=True,default=datetime.now())
    is_active = db.BooleanField(required=True,default= os.environ["APP_DEBUG"] == "false")

    @classmethod
    def get_user_by_email(cls,email):
        """ Get user object by email given 

        Args:
            email (str) : user email 

        Returns: 
            (app.models.user.User) : user object with the given email 
        """

        return cls.objects(email=email).first() 

    @classmethod 
    def create(cls,save=True,**kwargs):
        """Create a new user based on requested data 

        Args:
            email (string): 
                the user email

            password (string): 
                the unhashed user email 

            save (bool, optional):
                Whether or not to save the field and update ``comments_m2m``.

                If ``False``, the caller is responsible for performing the
                save.
            
            **kwargs (dict):
                Keyword arguments representing additional fields handled by
                the API resource. Any that are also listed in ``fields`` will
                be set on the model.

        Returns:
            app.models.user.User : new user just created
        """
        user_kwargs = {
            'email': kwargs.get('email'),
            'password': app_bcrypt.generate_password_hash(kwargs.get('password')).decode('UTF-8'),
        }
        fields = ['first_name','last_name']
        for field in fields:
            user_kwargs[field] = kwargs.get(field) 
        
        new_user = User(**user_kwargs)

        if save:
            new_user.save() 

        return new_user 


    def is_active(self):
        """ Verify if user is active in production 

        Returns:
            Bool: true if the user is created in production, false otherwise
        """
        return self.is_active 

    def validate_user(self,password):
        """ Validate password for the current user object 

        Args:
            password (string) : unhashed password 

        Returns:
            Bool: true if the password is correct, false otherwise
        """
        return app_bcrypt.check_password_hash(self.password,password)  

        

