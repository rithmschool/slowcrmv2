from project import app, db, bcrypt
from project.users.models import User
from project.messages.models import Message
from flask_testing import TestCase
import unittest
from flask import json


class TestApp(TestCase):
    def _login_user(self, username, password):
        pass



if __name__ == '__main__':
    unittest.main()