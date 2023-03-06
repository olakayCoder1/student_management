
from student_management import db
from datetime import datetime


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class User(db.Model ):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    identifier = db.Column(db.String(50), unique=True)
    email =  db.Column( db.String(100) , nullable=False , unique=True )
    first_name = db.Column(db.String(100), nullable=False )
    last_name = db.Column(db.String(100), nullable=False )
    password_hash = db.Column(db.String(64) , nullable=False )
    password_reset_token = db.Column(db.String(64) , nullable=False )
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

    user_type = db.Column(db.String(10))

    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return self.email





class Admin(User):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    designation = db.Column(db.String(255))
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }


class Student(User):
    __tablename__ = 'students'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    admission_no = db.Column(db.String(20))
    courses = db.relationship('Course', secondary='student_course')
    grades = db.relationship('Grade', secondary='student_grade')
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

class Teacher(User):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    employee_no = db.Column(db.String(20))
    courses = db.relationship('Course', backref='teacher')
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    course_code = db.Column(db.String(10), unique=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    grade = db.relationship('Grade', secondary='course_grade')
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

class StudentCourse(db.Model):
    __tablename__ = 'student_course'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)
    def __init__(self, student_id, course_id, score):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score



class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)