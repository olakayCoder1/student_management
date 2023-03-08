import datetime
import asyncio 
from http import HTTPStatus
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, get_jwt_identity ,
    create_refresh_token
)
from werkzeug.security import (
    check_password_hash , 
    generate_password_hash
)
from flask import  request 
from flask_restx import Namespace, Resource
from student_management.models import(
     User , Student , Admin , Teacher 
)
from student_management import db 
from student_management.utils import (
    random_char , generate_reset_token ,
    MailServices
)

from .serializers import (
    login_fields_serializer, register_fields_serializer,
    password_reset_request_fields_serializer,
    password_reset_fields_serializer
) 




auth_namespace = Namespace('auth', description='Namespace for Authentication')

login_serializer = auth_namespace.model('Login serializer', login_fields_serializer)
register_serializer = auth_namespace.model('Register serializer', register_fields_serializer)
password_reset_request_serializer = auth_namespace.model('Password reset request serializer', password_reset_request_fields_serializer)
password_reset_serializer = auth_namespace.model('Password reset serializer', password_reset_fields_serializer)



# Route for registering a user 
@auth_namespace.route('/register')
class UserRegistrationView(Resource):

    @auth_namespace.expect(register_serializer)
    def post(self):
        data = request.get_json()
        # Check if user already exists
        user = User.query.filter_by(email=data.get('email', None)).first()
        if user:
            return {'message': 'User already exists'} , HTTPStatus.CONFLICT
        # Create new user
        identifier=random_char(10)  
        current_year =  str(datetime.datetime.now().year)
        match data.get('user_type'):
            case 'student':
                admission= 'STD@' + random_char(6) + current_year
                new_user =  Student(
                    email=data.get('email'), 
                    identifier=identifier,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    user_type = 'student',
                    password_hash = generate_password_hash(data.get('password')),
                    admission_no=admission
                    )
                
            case 'teacher':
                employee= 'TCH@' + random_char(6) + current_year
                new_user = Teacher(
                    email=data.get('email'), 
                    identifier=identifier,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    user_type = 'teacher',
                    password_hash = generate_password_hash(data.get('password')),
                    employee_no=employee
                    )
            case 'admin':
                designation= 'Principal'
                new_user = Admin(
                    email=data.get('email'), 
                    identifier=identifier,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    user_type = 'admin',
                    password_hash = generate_password_hash(data.get('password')),
                    designation=designation
                    )
            case _ :
                response = {'message': 'Invalid user type'}
                return response , HTTPStatus.BAD_REQUEST
        try:
            new_user.save()
        except:
            db.session.rollback()
            return {'message': 'An error occurred while saving user'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'User registered successfully as a {}'.format(new_user.user_type)}, HTTPStatus.CREATED



# Route for Token refresh 
@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Generate Refresh Token
        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus.OK


# Route for login user in( Authentication )
@auth_namespace.route('/login')
class UserLoginView(Resource):
    @auth_namespace.expect(login_serializer)
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            response = {'message': 'Invalid username or password'}
            return response, HTTPStatus.UNAUTHORIZED
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        response = {
            'access_token': access_token,
            'refresh_token': refresh_token, 
            }
        return response, HTTPStatus.OK



# Route for requesting a password reset
@auth_namespace.route('/reset_password_request')
class PasswordResetRequestView(Resource):
    @auth_namespace.expect(password_reset_request_fields_serializer)
    async def post(self):
        email = request.json.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a random password reset token
            token = generate_reset_token(36)
            user.password_reset_token = token
            db.session.commit()
            # Send a password reset email
            mail = asyncio.create_task(MailServices.forget_password_mail(user.email, token))

        return {
            'message': 'An email has been sent with instructions to reset your password.'
            }, HTTPStatus.OK


# Route for resetting the password
@auth_namespace.route('/reset_password/<token>')
class PasswordResetView(Resource):
    @auth_namespace.expect(password_reset_fields_serializer)
    def post(self):
        token = request.json.get('token')
        user = User.query.filter_by(password_reset_token=token).first()
        if not user:
            return {
                'message': 'Invalid or expired token. Please try again.'
                }, HTTPStatus.BAD_REQUEST
        password1 = request.json.get('password1')
        password2 = request.json.get('password2')
        if password1 == password2  :
            user.set_password(password2)
            user.password_reset_token = None
            db.session.commit()
            return {
                'message': 'Your password has been reset.'
                }, HTTPStatus.OK
        
        return {
                'message': 'Password does not match.'
                }, HTTPStatus.UNAUTHORIZED


