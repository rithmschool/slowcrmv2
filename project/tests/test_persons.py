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

    # Test creating a new person that passes all validators
    def testNewPerson(self):
        response = self.client.post('/persons/',
            data=dict(email='aaron.m.manley@gmail.com',
            phone="4087261650",
            name='Aaron',
            title='Awesome',
            description='I am an awesome person'
            ), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('persons/index.html')
        self.assertEqual(
            Person.query.filter_by(phone= "4087261650").first().name,
            'Aaron')
        self.assertFalse(Person.query.filter_by(phone= "4087261650").first().slow_lp,
            False)
        self.assertEqual(
            Person.query.filter_by(phone= "4087261650").first().email,
            'aaron.m.manley@gmail.com')
        self.assertEqual(
            Person.query.filter_by(phone= "4087261650").first().description,
            "I am an awesome person")

    # Test new person that fails form validation, should render persons/new
    def testNewPersonFailValidation(self):
        response = self.client.post('/persons/',
            data=dict(email='aaron.m.manley@gmail.com',
            phone="",
            name='',
            title='Awesome',
            description='I am an awesome person'
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('persons/new.html')

    def testEditUser(self):
        # create new user to test editing on
        new_person = self.client.post('/persons/',
            data=dict(email='aaron.m.manley@gmail.com',
            phone="4087261650",
            name='Aaron',
            title='Awesome',
            description='I am an awesome person'
            ))

        response = self.client.post('/persons/1?_method=PATCH',
            data=dict(email='notaaron@rithmschool.com',
            phone="9992223333",
            title='Murky',
            name='Aaron',
            description='I am a Frog')
            ,follow_redirects=True
            )

        self.assertEqual(len(Person.query.all()), 1)
        self.assertEqual(response.status_code,200)
        self.assert_template_used('persons/show.html')
        self.assertEqual(
            Person.query.filter_by(phone= "9992223333").first().id,
            1)
        self.assertEqual(
            Person.query.filter_by(phone= "9992223333").first().name,
            'Aaron')
        self.assertFalse(Person.query.filter_by(phone= "9992223333").first().slow_lp,
            False)
        self.assertEqual(
            Person.query.filter_by(phone= "9992223333").first().email,
            'notaaron@rithmschool.com')
        self.assertEqual(
            Person.query.filter_by(phone= "9992223333").first().description,
            'I am a Frog')

if __name__ == '__main__':
    unittest.main()
