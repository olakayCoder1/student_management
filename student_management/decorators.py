from flask_jwt_extended import get_jwt , verify_jwt_in_request
from functools import wraps
from flask import jsonify
from http import HTTPStatus
from student_management.models import User



# this function was included here to avoid circular import
def get_user_type(pk:int):
    """ Get the type a user belong 
    param:
        pk : user id
    """
    user = User.query.filter_by(id=pk).first()
    if user:
        return user.user_type
    return None




def admin_required():
    """
    A decorator to protect an endpoint with JSON Web Tokens.

    Any route decorated with this will require a user type of admin  to be present in the
    request before the endpoint can be called.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args,**kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if get_user_type(claims['sub']) == 'admin':
                return fn(*args,**kwargs)
            return jsonify({'msg':"Admin only!"}) , HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper





def staff_required():
    """
    A decorator to protect an endpoint with JSON Web Tokens.

    Any route decorated with this will require a user type of admin or teacher  to be present in the
    request before the endpoint can be called.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args,**kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_type(claims['sub']) == 'admin' or get_user_type(claims['sub']) == 'teacher':
                return fn(*args,**kwargs)
            return jsonify({'msg': "Staff Only!" }) , HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper



def teacher_required():
    """
    A decorator to protect an endpoint with JSON Web Tokens.

    Any route decorated with this will require a user type of teacher to be present in the
    request before the endpoint can be called.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args,**kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_type(claims['sub']) == 'teacher' :
                return fn(*args,**kwargs)
            return jsonify({'msg': "Student Only!" }) , HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


def student_required():
    """
    A decorator to protect an endpoint with JSON Web Tokens.

    Any route decorated with this will require a user type of student  to be present in the
    request before the endpoint can be called.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args,**kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_type(claims['sub']) == 'student' :
                return fn(*args,**kwargs)
            return jsonify({'msg': "Student Only!" }) , HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper