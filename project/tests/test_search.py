from flask_testing import TestCase
import unittest
from project.models import User, Company
from project import app, db

class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        self.password = 'password1'
        self.user = User('divya@gmail.com', 'Divya', self.password, '123456789', True, True)
        db.session.add(self.user)
        db.session.commit()
        self.company = Company('Facebook')
        db.session.add(self.company)
        db.session.commit()
        self.login_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login_user(self):
        self.client.post('/users/login',
            data=dict(
                email=self.user.email,
                password=self.password
            )
        )

    def testSearch(self):
        url = '/users/search?search=Facebook'
        response = self.client.get(url,
            content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('users/search.html')


if __name__ == '__main__':
    unittest.main()