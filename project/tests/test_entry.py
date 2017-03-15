from flask_testing import TestCase
import unittest
from flask import json
from project.models import User
from datetime import datetime
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
        db.drop_all()

    def testNewEntry(self):
        response = self.client.post('/users/2/entries',
            data=dict(user_id=2,
                        content='working at Rithm',
                        created_at=datetime.utcnow,
                        updated_at=datetime.utcnow
            )
        )
        self.assertEqual(response.status_code, 200) 
        self.assert_template_used('users/entry.html')       

if __name__ == '__main__':
    unittest.main()        