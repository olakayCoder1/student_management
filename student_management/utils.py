from flask_sqlalchemy import SQLAlchemy
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import string
import secrets



db = SQLAlchemy()



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


password='evctrejhhdkghsmy'
sender_email='olakaycoder1@gmail.com' 




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
    def forget_password_mail(receiver_email , token ):
        """
        Send a forget password mail instruction to user
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = "Reset your password"
        message["From"] = sender_email
        message["To"] = receiver_email
        reset_link = f'http://127.0.0.1:5000/password/{token}/reset'
        html = ('accounts/password-reset-mail.html', {'reset_link': reset_link})
        part = MIMEText(html, "html")
        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(part)
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
# Your password reset instructions
# Click the link below to reset your password
# If you did not request a password reset, please ignore this email