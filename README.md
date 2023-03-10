# Student Management Student

Note: This is currently under active development

## Table of Contents

- [Student Management Student](#student-management-student)
  - [Table of Contents](#table-of-contents)
  - [Live ( deployed version )](#live--deployed-version-)
  - [Testing Locally](#testing-locally)

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

Best of luck
