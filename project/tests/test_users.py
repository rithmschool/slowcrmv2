from flask_testing import TestCase
import unittest
from flask import json
from project.models import User
from project.users.token import generate_confirmation_token, confirm_token
from project import app, db, bcrypt

class BaseTestCase(TestCase):
    def _login_user(self,email,password,follow_redirects=False):
        return self.client.post('/users/login', 
            data=dict(email=email, 
            password=password), follow_redirects=follow_redirects)

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        user1 = User('aricliesenfelt@gmail.com', 'Aric Liesenfelt', 'password1', '9515706209', True, False)
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
        response = self._login_user('tommyhopkins@gmail.com','wrongpassword',True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/login.html')
        # Logging in Successfully
        response = self._login_user('tommyhopkins@gmail.com','password2',True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/home.html')      

    def testSendInvite(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        # Successful Invite
        response = self.client.post('/users/invite',
            data=json.dumps(dict(email='noreply.slowcrm@gmail.com', name='Tommy')), 
            content_type='application/json')
        expected_json = 'Invite Sent'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(),3)
        self.assertEqual(response.json, expected_json)
        # Unsuccessful Invite
        response = self.client.post('/users/invite',
            data=json.dumps(dict(name='Tommy')), 
            content_type='application/json')
        expected_json = 'Missing form info'
        self.assertEqual(response.status_code, 422)
        self.assertEqual(User.query.count(),3)
        self.assertEqual(response.json, expected_json)

    def testTokenValid(self):
        # Success when user is created but not confirmed
        user3 = User('testemail@gmail.com', 'Name', 'temppass', '', True, False)
        db.session.add(user3)
        db.session.commit()
        token = generate_confirmation_token('testemail@gmail.com')
        response = self.client.get('/users/confirm/{}'.format(token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(),3)
        self.assert_template_used('users/update.html')

    def testTokenMissingUser(self):
        # Fail Test when email not in db
        token = generate_confirmation_token('mail@gmail.com')
        response = self.client.get('/users/confirm/{}'.format(token)) 
        self.assertEqual(response.status_code, 404)

    def testTokenInvalid(self):    
        # Fail test when token invalid or expired
        response = self.client.get('/users/confirm/invalidtoken',
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/login.html')

    def testLogout(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.get('/users/logout')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/users/invite',
            data=json.dumps(dict(email='noreply.slowcrm@gmail.com', name='Tommy')), 
            content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def testEditSuccess(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.post('/users/2/edit?_method=PATCH', 
            data=dict(email='tommyhopkins@gmail.com', 
            password='password2', name='Bob', phone='4154241512'), follow_redirects=True)
        user = User.query.get(2)
        self.assertEqual(response.status_code,200)
        self.assertEqual(user.name,'Bob')
        self.assert_template_used('users/show.html')

    def testEditWrongPass(self):
        # The password put in doesn't match db password
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.post('/users/2/edit?_method=PATCH', 
            data=dict(email='tommyhopkins@gmail.com', 
            password='wrongpassword', name='Bob', phone='4154241512'), follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assert_template_used('users/edit.html')  

    def testEditNotAuthorized(self):
        # Logged in user trying to access another user's edit page
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.get('/users/1/edit', follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assert_template_used('users/home.html')  

    def testUpdateGet(self):
        # Successfully access the page when user is not yet confirmed
        self._login_user('aricliesenfelt@gmail.com','password1')
        response = self.client.get('/users/1/update')
        self.assertEqual(response.status_code,200)
        self.assert_template_used('users/update.html')

    def testUpdateGetFail(self):
        # Redirect to login when user already confirmed
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.get('/users/2/update', follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assert_template_used('users/login.html')

    def testUpdatePost(self):
        self._login_user('aricliesenfelt@gmail.com','password1')
        response = self.client.post('/users/1/update?_method=PATCH', 
            data=dict(email='aricliesenfelt@gmail.com', 
            password='newpassword', confirmpassword='newpassword', 
            name='NewName', phone='4154241512'), follow_redirects=True)
        user = User.query.filter_by(email='aricliesenfelt@gmail.com').first()
        self.assertEqual(response.status_code,200)
        self.assertEqual(user.name, 'NewName')
        self.assertEqual(user.confirmed, True)
        self.assert_template_used('users/home.html')

    def testUpdateFail(self):
        #Passwords do not match
        self._login_user('aricliesenfelt@gmail.com','password1')
        response = self.client.post('/users/1/update?_method=PATCH', 
            data=dict(email='aricliesenfelt@gmail.com', 
            password='newpassword', confirmpassword='wrongpassword', 
            name='NewName', phone='4154241512'))
        user = User.query.filter_by(email='aricliesenfelt@gmail.com').first()
        self.assertEqual(response.status_code,200)
        self.assertEqual(user.confirmed, False)
        self.assert_template_used('users/update.html')

    def testPasswordRecoverySendSuccess(self):
        # Successful when email exists in db
        response = self.client.post('/users/passwordreset',
        data=dict(email='tommyhopkins@gmail.com'), follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assert_template_used('users/login.html')

    def testPasswordRecoverySendFail(self):
        # Fail when email doesn't exists in db
        response = self.client.post('/users/passwordreset',
        data=dict(email='bademail@gmail.com'), follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assert_template_used('users/forgot.html')

    def testResetPWTokenValid(self):
        # Success when accessing page sent in email to reset pw
        token = generate_confirmation_token('aricliesenfelt@gmail.com')
        response = self.client.get('/users/passwordreset/{}'.format(token))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/password_recover.html')

    def testResetPWTokenInvalid(self):
        # Fail when token is invalid or expired
        response = self.client.get('/users/passwordreset/invalidtoken', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/login.html')

    def testEditPassword(self):
        # Logged In User Editing Password
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.post('/users/2/editpassword?_method=PATCH',
            data=dict(newpassword='newpass', confirmpassword='newpass',
            currentpassword='password2'), follow_redirects=True)
        user = User.query.filter_by(email='tommyhopkins@gmail.com').first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bcrypt.check_password_hash(user.password, 'newpass'),True)
        self.assert_template_used('users/show.html')

    def testEditPasswordNoAuth(self):
        # Logged In User Cannot Access Another's Reset PW page
        self._login_user('tommyhopkins@gmail.com','password2', follow_redirects=True)
        response = self.client.get('/users/1/editpassword')
        self.assertEqual(response.status_code, 302)
        self.assert_template_used('users/home.html')


if __name__ == '__main__':
    unittest.main()
