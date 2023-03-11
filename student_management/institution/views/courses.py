from student_management.models import ( Student, Course,  Teacher ,  StudentCourse , Score )
from student_management.decorators import ( staff_required , admin_required ,teacher_required , student_required )
from student_management import db 
from student_management.student.serializers import students_fields_serializer
from student_management.utils import random_char
from flask_restx import Namespace, Resource , fields
from http import HTTPStatus
from flask import request
from ..serializers_course import course_retrieve_fields_serializer
from flask_jwt_extended import jwt_required , get_jwt_identity



courses_namespace = Namespace('courses', description='Namespace for courses')

course_creation_serializer = courses_namespace.model(
    'Course creation serializer', {
        'name': fields.String(required=True, description="Course name"),
        'credit_hours': fields.Integer(description="Course credit hours"),
        'teacher_id': fields.Integer(required=True, description="Course teacher id"),
    }
)

student_course_register_serializer = courses_namespace.model(
    'Student Course Creation Serializer', {
        'student_id': fields.String(required=True, description="A student id"),
    }
)
 
students_serializer = courses_namespace.model( 'Student Serializer', students_fields_serializer)

course_teacher_serializer = courses_namespace.model(
    'Course Teacher serializer', {
        'identifier': fields.String( description='User email address'),
        'email': fields.String(required=True, description='User email address'),
        'first_name': fields.String(required=True, description="First name"),
        'last_name': fields.String(required=True, description="Lat name"),
        'employee_no': fields.String(required=True, description="Course teacher id"),
        'created_at': fields.DateTime( description="Course creation date"),
    }
)
course_retrieve_serializer = courses_namespace.model('Course Retrieval serializer', course_retrieve_fields_serializer)




@courses_namespace.route('')
class CoursesListView(Resource):

    @courses_namespace.marshal_with(course_retrieve_serializer)
    @courses_namespace.doc(
        description="""
            This endpoint is accessible to all users. 
            It allows the retrieval of all available courses
            """
    )
    @jwt_required()
    def get(self):
        """
        Retrieve all available courses
        """
        courses = Course.query.all()
        return courses , HTTPStatus.OK
    

    @courses_namespace.expect(course_creation_serializer) 
    @courses_namespace.doc(
        description="""
            This endpoint is accessible to an admin. 
            It allows admin create a new course
            """
    )
    @admin_required()
    def post(self):
        """
        Create a new course
        """
        data = request.get_json()
        teacher = Teacher.query.filter_by(id=data.get('teacher_id')).first()
        if teacher:
            code = random_char(10)
            course = Course(
                course_code=code,
                teacher_id=teacher.id,
                name=data.get('name'),
            )
            try:
                course.save()
                return {'message': 'Course registered successfully'}, HTTPStatus.CREATED
            except:
                return {'message': 'An error occurred while saving course'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'Invalid teacher id'}, HTTPStatus.BAD_REQUEST






@courses_namespace.route('/<int:course_id>')
class CourseRetrievalView(Resource):

    @courses_namespace.marshal_with(course_retrieve_serializer)
    def get(self, course_id ):
        """
        Retrieve a course
        """
        course = Course.get_by_id(course_id)
        return course , HTTPStatus.OK
    
    @courses_namespace.doc(
        description="""
            This endpoint is accessible to an admin. 
            It allows admin delete a course
            """
    )
    @admin_required()
    def delete(self, course_id):
        """
        Delete a course
        """
        course = Course.query.filter_by(course_id).first()
        if not course:
            return {'message':'Course does not exist'}, HTTPStatus.NOT_FOUND
        try:
            course.delete()
        except:
            db.session.rollback()
            return {'message': 'An error occurred while saving user'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return HTTPStatus.NO_CONTENT
    



@courses_namespace.route('/<int:course_id>/students/add_and_drop')
class CourseRetrievalView(Resource):


    @courses_namespace.expect(student_course_register_serializer)
    @courses_namespace.doc(
        description="""
            This endpoint is accessible to a teacher. 
            It allows teacher add a  student the their course
            """
    )
    @teacher_required()
    def post(self, course_id ):
        """
        Register a student to a course
        """
        data = request.get_json()
        student_id = data.get('student_id')
        # check if student and course exist
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(course_id).first()
        if not student or not course:
            return {'message': 'Student or course not found'}, HTTPStatus.NOT_FOUND
        if student:
            #check if student has registered for the course before
            get_student_in_course = StudentCourse.query.filter_by(student_id=student.id, course_id=course.id).first()
            if get_student_in_course:
                return {
                    'message':'{} has already registered for the course'.format(student.first_name)
                    } , HTTPStatus.OK
            # Register the student to the course
            add_student_to_course = StudentCourse(student_id=student.id, course_id=course.id)
            try:
                add_student_to_course.save()
                return {'message': 'Course registered successfully'} , HTTPStatus.CREATED
            except:
                db.session.rollback()
                return {'message': 'An error occurred while registering course'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'Student does not exist'} , HTTPStatus.NOT_FOUND
    


    @courses_namespace.doc(
        description="""
            This endpoint is accessible to a teacher. 
            It allows teacher remove a  student from their course
            """
    )
    @teacher_required()
    def delete(self, course_id):
        """
        Unregister a student course
        """
        data = request.get_json()
        student_id = data.get('student_id')
        # check if student and course exist
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(course_id).first()
        if not student or not course:
            return {'message': 'Student or course not found'}, HTTPStatus.NOT_FOUND
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
                    'message':'{} has not register for this course'.format(student.first_name)
                    } , HTTPStatus.BAD_REQUEST
    




@courses_namespace.route('/<int:course_id>/students')
class CourseStudentsListView(Resource):

    @courses_namespace.marshal_with(students_serializer) 
    @courses_namespace.doc(
        description="""
            This endpoint is accessible to an admin and a teacher. 
            It allows the retrieval of all students in a course
            """
    )
    @staff_required()
    def get(self, course_id ):
        """
        Retrieve all registered student in a course
        """
        course = Course.get_by_id(course_id)
        get_student_in_course = StudentCourse.get_students_in_course_by(course.id) 
        return get_student_in_course , HTTPStatus.OK



@courses_namespace.route('/grade')
class CoursesGradeListView(Resource):

    @courses_namespace.doc(
        description="""
            This endpoint is accessible to a student. 
            It allows student retrieve all registered courses grade
            """
    )
    @student_required()
    def get(self):
        """
        Retrieve all student courses grade
        """     
        authenticated_user_id = get_jwt_identity() 
        student = Student.query.filter_by(id=authenticated_user_id).first()  
        courses = StudentCourse.get_student_courses(student.id)
        response = []
        
        for course in courses:
            grade_response = {}
            score_in_course = Score.query.filter_by(student_id=student.id , course_id=course.id).first()
            grade_response['name'] = course.name
            if score_in_course:
                grade_response['score'] = score_in_course.score
                grade_response['grade'] = score_in_course.grade
            else:
                grade_response['score'] = None
                grade_response['grade'] = None 
            response.append(grade_response)
        return response , HTTPStatus.OK