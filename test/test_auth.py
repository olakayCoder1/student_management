import unittest
from app import app , create_app
from student_management.configurations import config_dict
from student_management.utils import db
import json

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        db.create_all()


    def tearDown(self) -> None:
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None

        



    def test_admin_registration(self):
        data = {'first_name':'Admin','last_name': 'AdminOne','email':'admin13@gmail.com','password':'password123', 'user_type':'admin'} 
        response = self.client.post('/auth/register',data=json.dumps(data) , content_type='application/json')
        self.assertEqual(response.status_code, 201)