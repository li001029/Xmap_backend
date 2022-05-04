import os
import re
from flask import render_template
from flask_mail import Message
from app.views import app_mail
from app.logger import logger

LOG = logger.get_root_logger(__name__)

def is_valid_email(email):
    if email is None:
        return False
    email_reg_exp = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
    return email_reg_exp.match(email)

def send_reset_password_link(recipient,token):
    """Send reset password email helper function 

    Args:
        recipient (app.models.user.User): requested user
        token (string) : reset jwt token
    """
    msg = Message() 
    msg.subject = "X-Map Reset Password"
    msg.add_recipient(recipient.email)
    if os.environ['APP_DEBUG'] == "true":
        msg.sender = ("X-Map",os.environ.get('EMAIL_USER'))
    msg.html = render_template('reset_password_email.html', user = recipient.first_name)

    LOG.debug("Send password reset password email to {} from {}".format(msg.recipients,msg.sender))
    
    app_mail.send(msg)



