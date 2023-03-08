from student_management.utils import db
from student_management.models import Grade , Admin , User
from werkzeug.security import generate_password_hash



def populate_db():
    users = [
        {'first_name':'Olanrewaju',
         'last_name': 'Kabeer',
         'email':'olakay@gmail.com',
         'password':'olakay',
         }
    ]
    print(User.query.count())
    if User.query.count() < 1:
        for user in users:
            admin = Admin(
                    email=user['email'], 
                    first_name=user['first_name'], 
                    last_name=user['last_name'], 
                    password_hash=generate_password_hash(user['password']),
                    user_type='admin',
                    designation='Principal'
                )
            try:
                admin.save()
            except:
                pass



