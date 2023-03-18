from flask_sqlalchemy import SQLAlchemy
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import smtplib
import string
import secrets 
from dotenv import load_dotenv
import os

db = SQLAlchemy()

load_dotenv()

def generate_reset_token(length):
    """ Generate a password reset token 
    param:
        length : length of token to be generated"""
    return secrets.token_hex(length)


def random_char(length):
    """ Generate a random string 
    param:
        length : length of string to be generated"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


sender_email =  os.getenv('EMAIL_SENDER')  
password = os.getenv('EMAIL_PASSWORD') 



def get_grade(score):
    """ Convert a score to corresponding grade """
    if score < 100 and score > 89:
        return 'A'
    elif score < 90 and score > 79:
        return 'B'
    elif score < 80 and score > 69:
        return 'C'
    elif score < 70 and score > 59:
        return 'D'
    elif score < 60 and score > 49:
        return 'E'
    elif score < 50 :
        return 'F'    
    else:
        return 'F'


def convert_grade_to_gpa(grade):
    """Convert a grade to the corresponding point value """
    if grade == 'A':
        return 4.0
    elif grade == 'B':
        return 3.3
    elif grade == 'C':
        return 2.3
    elif grade == 'D':
        return 1.3
    else:
        return 0.0


class MailServices():
    def forget_password_mail(*args , **kwargs ):
            receiver = kwargs['email']
            token = kwargs['token']
            receiver = kwargs['email']
            subject = "Password reset"
            body = f"""
                    we receive a request to reset your password\n
                    You can ignore if you don't make the request. Click the link below the to set new password.\n
                    http://127.0.0.1:5000/password-reset/{token}
                """

            em = EmailMessage()
            em["From"] = sender_email
            em["To"] = receiver
            em["subject"] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as connection:
                    connection.login(sender_email, password)
                    connection.sendmail(sender_email, receiver, em.as_string())
            except:
                pass
            return True
