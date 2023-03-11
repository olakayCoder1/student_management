from flask_restx import fields


password_reset_request_fields_serializer = {
    'email': fields.String(required=True, description='User email address'),
}

password_reset_fields_serializer = {
    'token': fields.String(required=True, description="Password reset token"),
    'password1': fields.String(required=True, description="Password"),
    'password2': fields.String(required=True, description="Confirm password"),
}

password_change_fields_serializer = {
    'password1': fields.String(required=True, description="Password"),
    'password2': fields.String(required=True, description="Confirm password"),
}



login_fields_serializer = {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
}


register_fields_serializer = {
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description="First name"),
    'last_name': fields.String(required=True, description="Lat name"),
    'password': fields.String(required=True, description="A password"),
}