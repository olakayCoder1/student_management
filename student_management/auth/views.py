from student_management.models import User
from student_management import db 
from flask import  request , jsonify
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
import random
import string
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash




auth_namespace = Namespace('auth', description='Namespace for Authentication')

# Route for registering a user 
@auth_namespace.route('/register')
class UserRegistrationView(Resource):

    def post():
        data = request.get_json()

        # Check if user already exists
        user = User.query.filter_by(email=data.get('email', None)).first()
        if user:
            return jsonify({'message': 'User already exists'}), 409
        # Create new user
        new_user = User(
            email=data.get('email'), 
            role='student', 
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            password_hash = generate_password_hash(data.get('password'))
            )
        
        match data.get('role'):
            case 'student':
                new_user.role = 'student'
            case 'teacher':
                new_user.role = 'teacher'
            case 'admin':
                new_user.role = 'admin'
            case _ :
                jsonify({'message': 'Invalid user role'}), 400
        try:
            new_user.save()
        except:
            db.session.rollback()
            jsonify({'message': 'An error occurred while saving user'}), 500
        return jsonify({'message': 'User registered successfully as a {}'.format(data.get('role'))}), 201



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

    def post():
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'message': 'Invalid username or password'}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200



# Route for requesting a password reset
@auth_namespace.route('/reset_password_request')
class PasswordResetRequestView(Resource):

    def post():
        email = request.json.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a random password reset token
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
            user.password_reset_token = token
            db.session.commit()
            # Send a password reset email
            # message = Message('Password Reset Request', sender='noreply@yourdomain.com', recipients=[user.email])
            # message.body = f"Please click the following link to reset your password: {url_for('reset_password', token=token, _external=True)}"
            # mail.send(message)

        return jsonify(
            {
            'message': 'An email has been sent with instructions to reset your password.'
            }), 200


# Route for resetting the password
@auth_namespace.route('/reset_password/<token>')
class PasswordResetView(Resource):

    def post(token):
        user = User.query.filter_by(password_reset_token=token).first()
        if not user:
            return jsonify(
                {
                'message': 'Invalid or expired token. Please try again.'
                }), 400
        password1 = request.json.get('password1')
        password2 = request.json.get('password2')
        if password1 == password2  :
            user.set_password(password2)
            user.password_reset_token = None
            db.session.commit()
            return jsonify(
                {
                'message': 'Your password has been reset.'
                }), 200
        
        return jsonify(
                {
                'message': 'Password does not match.'
                }), 401


