from flask_testing import TestCase
import unittest
from datetime import datetime
from project.models import Person
from project import app, db, bcrypt


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testNewPerson(self):
        response = self.client.post('/persons',
            data=dict(email='aaron.m.manley@gmail.com',
            phone='4087261650',
            name='Aaron',
            title='Awesome',
            description='I am an awesome person',
            slow_lp=True,
            created_at=datetime.now,
            updated_at=datetime.now
            ), follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('/persons/index.html')
        self.assertEqual(Person.query.filter_by(phone=4087261650).name, 'Aaron')

if __name__ == '__main__':
    unittest.main()
