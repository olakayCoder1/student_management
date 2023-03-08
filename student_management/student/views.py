from student_management import db
from flask import request
from student_management.models import Student, StudentCourse , User , Course
from flask_jwt_extended import jwt_required, get_jwt_identity  
from flask_restx import Namespace, Resource
from .serializers import (
    students_fields_serializer , course_fields_serializer
)
from student_management.institution.serializers_course import course_retrieve_fields_serializer
from http import HTTPStatus


students_namespace = Namespace('student', description='Namespace for Student ')



students_serializer = students_namespace.model('Students list serializer', students_fields_serializer)
courses_serializer = students_namespace.model('Students courses list serializer', course_retrieve_fields_serializer)
courses_add_serializer = students_namespace.model('Courses add serializer', course_fields_serializer)



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
        students = Student.get_by_id(student_id)
        return students , HTTPStatus.OK
     


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
    


    