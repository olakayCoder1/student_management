# Student Management Student

Note: This is currently under active development

## Table of Contents

- [Student Management Student](#student-management-student)
  - [Table of Contents](#table-of-contents)
  - [Live ( deployed version )](#live--deployed-version-)
  - [Testing Locally](#testing-locally)
  - [Available Endpoint](#available-endpoint)
    - [Auth Endpoint](#auth-endpoint)
    - [Students Endpoint](#students-endpoint)
    - [Courses Endpoint](#courses-endpoint)

## Live ( deployed version ) 

Visit [website](http://olakaycoder1.pythonanywhere.com/)
## Testing Locally

Clone the repository

```console
git clone https://github.com/olakayCoder1/student_management.git
```

Change directory to the cloned folder

```console
cd student_management
```

Install necessary dependency to run the project

```console
pip install -r requirements.txt
```
Create database from migration files 

```console
flask db migrate -m "your description"
```

```console
flask db upgrade
```
Run application

```console
flask run
```

To populate the database with some data navigate to student_management/auth/views in your code editor and uncomment the
populate_db function in the `UserLoginView` then make a post request to this endpoint `http://127.0.0.1:5000/auth/login`.
Make sure to comment back or delete the line  `# populate_db()`

```python
@auth_namespace.route('/login')
class UserLoginView(Resource):
    @auth_namespace.expect(login_serializer)
    @auth_namespace.doc(
        description="""
            This endpoint is accessible only to all user. 
            It allows user authentication
            """
    )
    def post(self):
        """ Authenticate a user"""
        # populate_db()
        email = request.json.get('email')
        password = request.json.get('password')
    .........
```

The action perform will create an admin user , two teacher and two student with the following credentials

| USER TYPE | FIRST NAME | LAST NAME | EMAIL | PASSWORD |
| ------- | ----- | ------|------- | ----- |
| __Admin__ | Admin  | AdminOne | admin1@gmail.com | _password123_ |
| __Teacher__ | Teacher  | TeacherOne | teacher1@gmail.com | _password123_ |
| __Teacher__ | Teacher  | TeacherTwo | teacher2@gmail.com | _password123_ |
| __Student__ | Student  | StudentOne | student1@gmail.com | _password123_ |
| __Student__ | Student  | StudentTwo | student2@gmail.com | _password123_ |

also with two courses `Mathematics` and `Geography`

The student created will then be register to Mathematics course.

Continue testing......



## Available Endpoint

### Auth Endpoint
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `auth/register` | _POST_ | It allows the  creation of a student account   | Any | Any |  ---- | 
|  `auth/register/teacher` |  _POST_ | It allows the creation of a teacher account   | Authenticated | Admin | ---- | 
|  `auth/token` |  _POST_  | It allows user authentication   | Any | Any | ---- | 
|  `auth/token/refresh` |  _POST_  | It allows user refresh their tokens   | Authenticated | Any | ---- | 
|  `auth/password-reset/<token>` |  _POST_  | It allows user reset new password  | Any | Any | A reset token | 
|  `auth/password-reset-request` |  _POST_  | It allows user request new password if they forget their password | Any | Any |  ---- | 
|  `auth/password-change` |  _POST_  | It allows user change new password | Authenticated | Any |---- |


### Students Endpoint
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `students` |  _GET_  | It allows the retrieval all student is the school   | Authenticated | Admin | ---- |
|  `students/<student_id>` |  _GET_  | It allows the  retrieval of a student | Authenticated | Any | A student ID |
|  `students/<student_id>/courses/grade` |  _GET_  | It allows the retrieval a student all courses grade   | Authenticated | Any | A student ID |
|  `students/<student_id>/courses` |  _GET_  | It allows the retrieval of a student courses   | Authenticated | ---- | A student ID |
|  `students/<student_id>/gpa` |  _GET_  | Calculate a student gpa score   | Authenticated | Any | A student ID |
|  `students/courses/add_and_drop` |  _POST_  | It allows student register a course   | Authenticated | Student | ---- |
|  `students/courses/add_and_drop` |  _DELETE_  | It allows student unregister a course   | Authenticated | Student | ---- |
|  `students/course/add_score` |  _PUT_  | It allow teacher add a student score in a course | Authenticated | Teacher | ---- |


### Courses Endpoint
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `courses` |  _GET_  | It allows the retrieval of all available courses   | Authenticated | Any | ---- |
|  `courses` |  _POST_  | It allows the creation of a new course   | Authenticated | Admin | ---- |
|  `courses` |  _DELETE_  | It allows deleting a course   | Authenticated | Admin | ---- |
|  `courses/<course_id>` |  _GET_  | It allows the retrieval all student is the school   | Authenticated | Admin | A course ID |
|  `courses/<course_id>/students` |  _GET_  | It allows the  retrieval of all students in a courses | Authenticated | Any | A course ID |
|  `courses/<course_id>/students/add_and_drop` |  _POST_  | It allows teacher add a  student the their course | Authenticated | Teacher | A course ID |
|  `courses/<course_id>/students/add_and_drop` |  _DELETE_  | It allows teacher remove a  student from their course | Authenticated | Teacher | A course ID |
|  `courses/grade` |  _GET_  | It allows student retrieve all registered courses grade | Authenticated | Student | ---- |



