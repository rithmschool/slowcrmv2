from flask_testing import TestCase
import unittest
from flask import json
from project.models import User, Tag
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

    def testPostingAutocompleteTag(self):
        url = '/users/search/autocomplete?params=*a'
        response = self.client.get(url,
            content_type = 'application/json'
        ) 
        tag = Tag.query.get(self.tag2.id)
        self.assertEqual(response.json['suggestions'][0]['value'], "*"+tag.text+"*")


if __name__ == '__main__':
    unittest.main()        