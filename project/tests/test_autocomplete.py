from flask_testing import TestCase
import unittest
from project.models import User, Tag, Company, Person
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
        tag1 = Tag('tag')
        self.tag2 = Tag('another tag')
        db.session.add(tag1)
        db.session.commit()
        db.session.add(self.tag2)
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

    def test_tag_autocomplete_no_specialchars(self):
        url = '/tags/autocomplete?params=a'
        response = self.client.get(url,
            content_type='application/json'
        )
        tag = Tag.query.get(self.tag2.id)
        self.assertEqual(response.json['suggestions'][0]['value'], tag.text)

    def test_tag_autocomplete_with_specialchars(self):
        url = '/tags/autocomplete?params=*a&specialchars=1'
        response = self.client.get(url,
            content_type='application/json'
        )
        tag = Tag.query.get(self.tag2.id)
        self.assertEqual(response.json['suggestions'][0]['value'], '*'+tag.text+'*')

    def test_company_autocomplete(self):
        google = Company('Google')
        db.session.add(google)
        db.session.commit()
        url = '/tags/autocomplete?params=%24g&specialchars=1'
        response = self.client.get(url,
            content_type='application/json'
        )
        company = Company.query.get(1)
        self.assertEqual(response.json['suggestions'][0]['value'], '$'+company.name+'$')

    def test_person_autocomplete(self):
        tim = Person('Tim')
        db.session.add(tim)
        db.session.commit()
        url = '/tags/autocomplete?params=%7Ct&specialchars=1'
        response = self.client.get(url,
            content_type='application/json'
        )
        from IPython import embed; embed()
        person = Person.query.get(1)
        self.assertEqual(response.json['suggestions'][0]['value'], '|'+person.name+'|')

if __name__ == '__main__':
    unittest.main()
