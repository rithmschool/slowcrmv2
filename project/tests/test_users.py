from flask_testing import TestCase
import unittest
from flask import json
from project.models import User
from project import app, db, bcrypt


class BaseTestCase(TestCase):
    render_templates = False
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        user1 = User('aricliesenfelt@gmail.com', 'Aric Liesenfelt', 'password1', '9515706209', True, True)
        user2 = User('tommyhopkins@gmail.com', 'Tommy Hopkins', 'password2', '1111111111', True, True)  
        db.session.add_all([user1,user2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()



    def testSendInvite(self):
        # Successful Invite
        response = self.client.post('/users/invite',
            data=json.dumps(dict(email='hopmailkins@gmail.com', name='Tommy')), 
            content_type='application/json', follow_redirects=True)

        expected_json = 'Invite Sent'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_json)
        


if __name__ == '__main__':
    unittest.main()
