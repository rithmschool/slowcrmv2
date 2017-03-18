from flask_testing import TestCase
import unittest
from flask import json
from project.models import User
from project import app, db
from project.models import Entry

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

    def testNewEntry(self):
        content = "Here I am"
        response = self.client.post('/users/entries',
            data=json.dumps(dict(
                content=content,
            )),
            content_type='application/json'
        )
        entry_id = response.json['entry_id']
        entry = Entry.query.get(entry_id)
        self.assertEqual(entry.content, content)
        self.assertEqual(response.status_code, 200) 

    def testEntryEmpty(self):    
        content = ""
        with self.assertRaises(ValueError) as e:
            self.client.post('/users/entries',
                data=json.dumps(dict(
                    content=content
                )),
                content_type='application/json'
            )
            self.assertEqual(e.message, 'content is empty')

    def testNewPersonInEntry(self):
        person_name = 'Sundar'
        content = "|{}| is a Google CEO".format(person_name)
        response = self.client.post('/users/entries',
            data=json.dumps(dict(
                content=content,
            )),
            content_type='application/json'
        )
        entry_id = response.json['entry_id']
        entry = Entry.query.get(entry_id)
        person_from_db = [p.name for p in entry.persons]
        self.assertEqual(person_from_db, [person_name])
        self.assertEqual(response.status_code, 200)


    def testNewPersonCompanyInEntry(self):
        content = "|Sundar| is a $Google$ CEO and |Satya| is a $Microsoft$ CEO"
        response = self.client.post('/users/entries',
            data=json.dumps(dict(
                content=content,
            )),
            content_type='application/json'
        )
        entry_id = response.json['entry_id']
        entry = Entry.query.get(entry_id)
        person_from_db = [p.name for p in entry.persons]
        company_from_db = [c.name for c in entry.companies]
        self.assertEqual(person_from_db, ['Sundar', 'Satya'])
        self.assertEqual(company_from_db, ['Google', 'Microsoft'])
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
