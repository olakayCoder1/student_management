from flask_restx import fields



course_retrieve_fields_serializer =  {
    'id': fields.Integer(),
    'name': fields.String(required=True, description="A course name"),
    'course_code': fields.String(description="A course code"),
    'teacher_id': fields.Integer(), 
    'created_at': fields.DateTime( description="Course creation date"),
}


