from flask_sqlalchemy import SQLAlchemy
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import environ
from email.message import EmailMessage
import smtplib
import os  
db = SQLAlchemy()
import string
import secrets



def generate_reset_token(length):
    return secrets.token_hex(length)


def random_char(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

sender_email = os.getenv('EMAIL_SENDER')
password = os.getenv('EMAIL_PASSWORD')




def convert_grade_to_gpa(grade):
    if grade == 'A':
        return 4.0
    elif grade == 'A-':
        return 3.7
    elif grade == 'B+':
        return 3.3
    elif grade == 'B':
        return 3.0
    elif grade == 'B-':
        return 2.7
    elif grade == 'C+':
        return 2.3
    elif grade == 'C':
        return 2.0
    elif grade == 'C-':
        return 1.7
    elif grade == 'D+':
        return 1.3
    elif grade == 'D':
        return 1.0
    else:
        return 0.0


class MailServices():
    def forget_password_mail(receiver_email , token ):
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