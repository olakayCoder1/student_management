from student_management.utils import db
from .auth.views import auth_namespace
from student_management.student.views import  students_namespace
from student_management.institution.views.courses import  courses_namespace
from .models import (
    User,Teacher,Course,
    Score,Admin,
    Student,StudentCourse)
from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate 
from student_management.configurations import config_dict
from pathlib import Path 
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }

    api = Api(
        app,
        title='Student Management System API',
        description='A student management system REST API service',
        authorizations=authorizations, 
        security='Bearer Auth'
        )


    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(students_namespace, path='/students')
    api.add_namespace(courses_namespace, path='/courses')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 404

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Teacher': Teacher,
            'Score': Score,
            'Admin': Admin,
            'Student': Student,
            'StudentCourse': StudentCourse,
            'Course': Course,
        }


    
    return app