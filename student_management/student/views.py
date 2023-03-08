from student_management import db
from flask import request
from student_management.models import Student, StudentCourse , User , Course , Score , Grade
from flask_jwt_extended import jwt_required, get_jwt_identity  
from flask_restx import Namespace, Resource
from .serializers import (
    students_fields_serializer , 
    course_fields_serializer,
    student_score_add_fields_serializer
)
from student_management.utils import convert_grade_to_gpa
from student_management.institution.serializers_course import course_retrieve_fields_serializer
from http import HTTPStatus


students_namespace = Namespace('student', description='Namespace for Student ')



students_serializer = students_namespace.model('Students list serializer', students_fields_serializer)
courses_serializer = students_namespace.model('Students courses list serializer', course_retrieve_fields_serializer)
courses_add_serializer = students_namespace.model('Courses add serializer', course_fields_serializer)
student_score_add_serializer = students_namespace.model('Courses add serializer', student_score_add_fields_serializer)



# Route for login user in( Authentication )
@students_namespace.route('')
class StudentsListView(Resource):

    @students_namespace.marshal_with(students_serializer)
    @students_namespace.doc(
        description=' jhghjkl'
    )
    def get(self):
        students = Student.query.all()
        return students , HTTPStatus.OK




@students_namespace.route('/<int:student_id>')
class StudentRetrieveDeleteUpdateView(Resource):

    @students_namespace.marshal_with(students_serializer)
    def get(self, student_id):
        """
        Retrieve a student 
        """
        student = Student.get_by_id(student_id)
        return student , HTTPStatus.OK
     


@students_namespace.route('/<int:student_id>/courses')
class StudentCoursesListView(Resource):

    @students_namespace.marshal_with(courses_serializer)
    def get(self, student_id):
        """
        Retrieve a student courses
        """     
        courses = StudentCourse.get_student_courses(student_id)
        return courses , HTTPStatus.OK


@students_namespace.route('/course/add_and_drop')
class StudentCourseRegisterView(Resource):

    @students_namespace.marshal_with(courses_serializer)
    @students_namespace.expect(courses_add_serializer)
    @jwt_required()  
    def post(self):
        """ 
        Register for a course 
        """     
        authenticated_user_id = get_jwt_identity()
        user = User.get_by_id(authenticated_user_id)
        if user.user_type != 'student':
            return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        data = request.get_json()
        course = Course.get_by_id(data.get('course_id'))
        student = Student.query.filter_by(id=user.id).first()
        if student:
            #check if student has registered for the course before
            get_student_in_course = StudentCourse.query.filter_by(student_id=student.id, course_id=course.id).first()
            if get_student_in_course:
                return {
                    'message':'Course has already been registered'
                    } , HTTPStatus.OK
            # Register the student to the course
            add_student_to_course = StudentCourse(student_id=user.id, course_id=course.id)
            try:
                add_student_to_course.save()
                return {'message': 'Course registered successfully'} , HTTPStatus.CREATED
            except:
                db.session.rollback()
                return {'message': 'An error occurred while registering course'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'Student does not exist'} , HTTPStatus.NOT_FOUND


    @students_namespace.expect(courses_add_serializer)
    @jwt_required()
    def delete(self):
        """
        Unregister a  course
        """
        data = request.get_json()
        authenticated_user_id = get_jwt_identity()
        user = User.get_by_id(authenticated_user_id)
        if user.user_type != 'student':
            return {'message':'You are not authorized to the endpoint'}, HTTPStatus.UNAUTHORIZED
        student = Student.query.filter_by(id=user.id).first()
        course = Course.get_by_id(data.get('course_id'))
        if student:
            #check if student has registered for the course before
            get_student_in_course = StudentCourse.query.filter_by(student_id=student.id, course_id=course.id).first()
            if get_student_in_course:
                try:
                    get_student_in_course.delete()
                    return {'message': 'Course delete successfully'} , HTTPStatus.NO_CONTENT
                except:
                    db.session.rollback()
                    return {'message': 'An error occurred while delete student course'}, HTTPStatus.INTERNAL_SERVER_ERROR
            return {
                    'message':'You have not register for this course'
                    } , HTTPStatus.BAD_REQUEST
    


@students_namespace.route('/course/add_score')
class StudentCourseScoreAddView(Resource):

    @students_namespace.expect(student_score_add_serializer)
    def post(self):
        """
        Add a student course score
        """     
        student_id = request.json['student_id']
        course_id = request.json['course_id']
        score_value = request.json['score']
        # check if student and course exist
        student = Student.query.get(student_id)
        course = Course.query.get(course_id)
        if not student or not course:
            return {'message': 'Student or course not found'}, HTTPStatus.NOT_FOUND
        # check if student is registered for the course
        student_in_course = StudentCourse.query.filter_by(course_id=course.id, student_id=student.id).first() 
        if student_in_course:
            # check if the student already have a score in the course
            score = Score.query.filter_by(student_id=student_id, course_id=course_id).first()
            if score:
                score.score = score_value
            else:
                # create a new score object and save to database
                score = Score(student_id=student_id, course_id=course_id, score=score_value)
            try:
                score.save()
                return {'message': 'Score added successfully'}, HTTPStatus.CREATED
            except:
                db.session.rollback()
                return {'message': 'An error occurred while saving student course score'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'The student is not registered for this course'}, HTTPStatus.BAD_REQUEST

     



@students_namespace.route('/<int:student_id>/gpa')
class StudentGPAView(Resource):


    def post(self, student_id):
        """
        Calculate a student gpa score
        """     
        student = Student.get_by_id(student_id)
        courses = StudentCourse.get_student_courses(student.id)
        total_weighted_gpa = 0
        total_credit_hours = 0
        for course in courses:
            score_exist = Score.query.filter_by(student_id=student.id, course_id=course.id).first()
            if score_exist:
                score = score_exist.score
                gpa = convert_grade_to_gpa(score)
                weighted_gpa = gpa * course.credit_hours
                total_weighted_gpa += weighted_gpa
                total_credit_hours += course.credit_hours
        if total_credit_hours == 0:
            return {
                'message':'GPA calculation completed',
                'gpa': total_credit_hours
            }, HTTPStatus.OK
        else:
            gpa =  total_weighted_gpa / total_credit_hours
            return {
                'message':'GPA calculation completed',
                'gpa': gpa
            }, HTTPStatus.OK

        