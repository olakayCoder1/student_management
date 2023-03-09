from student_management.models import Admin , Teacher , Course ,Student , StudentCourse
from werkzeug.security import generate_password_hash
from student_management.utils import ( random_char )
import datetime 


def populate_db():
    admins = [
        {'first_name':'Admin','last_name': 'AdminOne','email':'admin1@gmail.com','password':'password123',},
        {'first_name':'Admin','last_name': 'AdminTwo','email':'admin2@gmail.com','password':'password123',},
    ]
    teachers = [
        {'first_name':'Teacher','last_name': 'TeacherOne','email':'teacher1@gmail.com','password':'password123',},
        {'first_name':'Teacher','last_name': 'TeacherTwo','email':'teacher2@gmail.com','password':'password123',},
    ]
    students = [
        {'first_name':'Student','last_name': 'StudentOne','email':'student1@gmail.com','password':'password123',},
        {'first_name':'Student','last_name': 'StudentTwo','email':'student2@gmail.com','password':'password123',},
    ]
    courses = [
        {'course_code':'MAT564','credit_hours': 3,'name':'Math'},
        {'course_code':'GHT538','credit_hours': 1,'name':'Geo'},
    ]
    for user in admins:
        identifier=random_char(10)  
        current_year =  str(datetime.datetime.now().year)
        admin = Admin(email=user['email'],first_name=user['first_name'],last_name=user['last_name'], 
                    password_hash=generate_password_hash(user['password']),user_type='admin',
                    designation='Principal', identifier=identifier
                )
        try:
            admin.save()
        except:
            pass

    for user in teachers:
        identifier=random_char(10)  
        current_year =  str(datetime.datetime.now().year)
        employee_no= 'TCH@' + random_char(6) + current_year
        admin = Teacher(email=user['email'],first_name=user['first_name'],last_name=user['last_name'], 
                    password_hash=generate_password_hash(user['password']),user_type='teacher', 
                    employee_no=employee_no, identifier=identifier
                )
        try:
            admin.save()
        except:
            pass

    
    for course in courses:
        teacher = Teacher.query.filter_by(email='teacher1@gmail.com')
        data = Course(course_code=course['course_code'],credit_hours=course['credit_hours'],
                       name=course['name'], teacher_id=teacher.id
                )
        try:
            data.save()
        except:
            pass

    for user in students:
        identifier=random_char(10)  
        current_year =  str(datetime.datetime.now().year)
        admission_no= 'STD@' + random_char(6) + current_year
        student = Student(email=user['email'],first_name=user['first_name'],last_name=user['last_name'], 
                    password_hash=generate_password_hash(user['password']),user_type='student', 
                    admission_no=admission_no, identifier=identifier
                )
        try:
            student.save()
            course = Course.query.filter_by(course_code='MAT564').first()
            student_course = StudentCourse(student_id=student.id, course_id=course.id)
            student_course.save() 
        except:
            pass



populate_db()