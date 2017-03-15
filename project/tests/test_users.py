from flask_testing import TestCase
import unittest
from flask import json
from project.models import User
from project.users.token import generate_confirmation_token, confirm_token
from project import app, db, bcrypt

class BaseTestCase(TestCase):
    
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True
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

    def testLogin(self):
        # Accessing login page
        self.client.get('/users/login')
        self.assert_template_used('users/login.html')
        # Wrong Password
        response = self.client.post('/users/login', 
            data=dict(email='tommyhopkins@gmail.com', 
            password='wrongpassword'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/login.html')
        # Logging in Successfully
        response = self.client.post('/users/login', 
            data=dict(email='tommyhopkins@gmail.com', 
            password='password2'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/home.html')      

    def testSendInvite(self):
        # Successful Invite
        response = self.client.post('/users/invite',
            data=json.dumps(dict(email='noreply.slowcrm@gmail.com', name='Tommy')), 
            content_type='application/json', follow_redirects=True)
        expected_json = 'Invite Sent'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(),3)
        self.assertEqual(response.json, expected_json)
        # Unsuccessful Invite
        response = self.client.post('/users/invite',
            data=json.dumps(dict(name='Tommy')), 
            content_type='application/json', follow_redirects=True)
        expected_json = 'Missing form info'
        self.assertEqual(response.status_code, 422)
        self.assertEqual(User.query.count(),3)
        self.assertEqual(response.json, expected_json)

    def testTokenValidation(self):
        # Fail Test when email not in db
        token = generate_confirmation_token('mail@gmail.com')
        response = self.client.get('/users/confirm/{}'.format(token)) 
        self.assertEqual(response.status_code, 404)
        # Fail test when token invalid or expired
        response = self.client.get('/users/confirm/invalidtoken',
            follow_redirects=True)
        self.assert_template_used('users/login.html')
        # Success when user is created but not confirmed
        user3 = User('testemail@gmail.com', 'Name', 'temppass', '', True, False)
        db.session.add(user3)
        db.session.commit()
        token = generate_confirmation_token('testemail@gmail.com')
        response = self.client.get('/users/confirm/{}'.format(token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(),3)
        self.assert_template_used('users/edit.html')
        # Test when email is already confirmed
        user4 = User('confirmedemail@gmail.com', 'Name', 'temppass', '', True, True)
        db.session.add(user4)
        db.session.commit()
        token = generate_confirmation_token('confirmedemail@gmail.com')
        response = self.client.get('/users/confirm/{}'.format(token), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(),4)
        self.assert_template_used('users/login.html')





if __name__ == '__main__':
    unittest.main()
