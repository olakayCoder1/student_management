from student_management import app, db
from flask import request, jsonify
from student_management.models import Student, Course, Score , User , Grade
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity  


@app.route('/scores', methods=['POST'])
@jwt_required()
# @roles_required('admin')
def add_score():
    student_id = request.json['student_id']
    course_id = request.json['course_id']
    score_value = request.json['score']
    
    # check if student and course exist
    student = Student.query.get(student_id)
    course = Course.query.get(course_id)
    if not student or not course:
        return jsonify({'error': 'Student or course not found'}), 404
    
    # check if the student is registered for the course
    if student not in course.students:
        return jsonify({'error': 'Student is not registered for this course'}), 400
    
    # create a new score object and save to database
    score = Score(student_id=student_id, course_id=course_id, value=score_value)
    db.session.add(score)
    db.session.commit()
    
    return jsonify({'message': 'Score added successfully'}), 201

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({'message': f'Hello, {user.username}!'})



def calculate_gpa(student):
    courses = Course.query.filter(Course.students.any(id=student.id)).all()
    total_weighted_gpa = 0
    total_credit_hours = 0
    for course in courses:
        grade = Grade.query.filter_by(student_id=student.id, course_id=course.id).first().grade
        gpa = convert_grade_to_gpa(grade)
        weighted_gpa = gpa * course.credit_hours
        total_weighted_gpa += weighted_gpa
        total_credit_hours += course.credit_hours
    if total_credit_hours == 0:
        return 0
    else:
        return total_weighted_gpa / total_credit_hours

def convert_grade_to_gpa(grade):
    if grade == 'A':
        return 4.0
    elif grade == 'A-':
        return 3.7
    elif grade == 'B+':
        return 3.3
    elif grade == 'B':
        return 3.0
    elif grade == 'B-':
        return 2.7
    elif grade == 'C+':
        return 2.3
    elif grade == 'C':
        return 2.0
    elif grade == 'C-':
        return 1.7
    elif grade == 'D+':
        return 1.3
    elif grade == 'D':
        return 1.0
    else:
        return 0.0
