from flask_restx import fields



students_fields_serializer = {
    'id': fields.String(),
    'identifier': fields.String(required=False, description='User identifier'),
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description="First name"),
    'last_name': fields.String(required=True, description="Lat name"),
    'admission_no': fields.String(required=True, description="First name"),
}



course_fields_serializer = {
    'course_id': fields.String(required=True),
}