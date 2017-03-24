from flask_testing import TestCase
import unittest
from project.models import Tag, User
from project import app, db

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
        tag1 = Tag('tag')
        db.session.add_all([user1,user2, tag1])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testNewTagForm(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.get('/tags/new', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('tags/new.html')

    def testTagIndex(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.get('/tags', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('tags/index.html')    

    def testAddNewTag(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.post('/tags/',
            data=dict(tag='newtag'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tag.query.count(), 2)
        self.assert_template_used('tags/index.html')

    def testAddTagAlreadyExists(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.post('/tags/',
            data=dict(tag='tag'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tag.query.count(), 1)
        self.assert_template_used('tags/index.html')   


if __name__ == '__main__':
    unittest.main()        