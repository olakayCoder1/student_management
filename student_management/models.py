from .utils import db
from datetime import datetime



class User(db.Model ):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    identifier = db.Column(db.String(50), unique=True , nullable=False )
    email =  db.Column( db.String(100) , nullable=False , unique=True )
    first_name = db.Column(db.String(100), nullable=False )
    last_name = db.Column(db.String(100), nullable=False )
    password_hash = db.Column(db.String(64) , nullable=False )
    password_reset_token = db.Column(db.String(64) , nullable=True )
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

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def __repr__(self) -> str:
        return self.email





class Admin(User):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    designation = db.Column(db.String(255) , nullable=True  )
    rc_number = db.Column(db.Integer, nullable=False)
    school_mail =  db.Column( db.String(100) , nullable=False , unique=True )
    is_superadmin = db.Column( db.Boolean , default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Student(User):
    __tablename__ = 'students'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    admission_no = db.Column(db.String(20))
    courses = db.relationship('Course', secondary='student_course')
    score = db.relationship('Score', backref='student_score', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


class Teacher(User):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    employee_no = db.Column(db.String(20))
    courses = db.relationship('Course', backref='teacher_course')

    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    course_code = db.Column(db.String(10), unique=True)
    credit_hours = db.Column(db.Integer, default=1) 
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()






class StudentCourse(db.Model):
    __tablename__ = 'student_course'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    

    @classmethod
    def get_students_in_course_by(cls, course_id):
        students = (
            Student.query.join(StudentCourse)
            .join(Course).filter(Course.id == course_id).all()
        )
        return students
    

    @classmethod
    def get_student_courses(cls, student_id):
        courses = (
            Course.query.join(StudentCourse)
            .join(Student).filter(Student.id == student_id).all()
        )
        return courses
    




class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    score = db.Column(db.Float , nullable=False)
    grade = db.Column(db.String(5) , nullable=True )
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)



    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
