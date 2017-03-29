from flask_testing import TestCase
import unittest
from project.models import User, Company, Person, Tag, Entry
from project import app, db

class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.password = 'password1'
        self.user = User('divya@gmail.com', 'Divya', self.password, '123456789', True, True)
        db.session.add(self.user)
        db.session.commit()
        self.company = Company('Facebook')
        db.session.add(self.company)
        db.session.commit()
        self.company2 = Company('Oracle')
        db.session.add(self.company2)
        db.session.commit()
        self.person = Person('Mark Zuckerberg')
        db.session.add(self.person)
        db.session.commit()
        self.person2 = Person('Bill Gates')
        db.session.add(self.person2)
        db.session.commit()
        self.tag = Tag("messenger")
        db.session.add(self.tag)
        db.session.commit()
        self.login_user()
        self.entry = Entry(1, "some content")
        db.session.add(self.entry)
        db.session.commit()

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

    def testCompanySearchResults(self):
        url = '/users/search?search=Facebook'
        response = self.client.get(url,
            content_type='application/json')
        to_utf_arr = response.data.decode("utf-8").split()
        self.assertEqual(self.find_result( to_utf_arr, "Facebook"), True)
        self.assertEqual(self.find_result(to_utf_arr, "orangutan"), False)

    def testPersonSearchResults(self):
        url = '/users/search?search=Mark'
        response = self.client.get(url,
            content_type='application/json')
        to_utf_arr = response.data.decode("utf-8").split()
        self.assertEqual(self.find_result( to_utf_arr, "Mark"), True)
        self.assertEqual(self.find_result(to_utf_arr, "orangutan"), False)

    def testTagSearchResults(self):
        url = '/users/search?search=messenger'
        response = self.client.get(url,
            content_type='application/json')
        to_utf_arr = response.data.decode("utf-8").split()
        self.assertEqual(self.find_result( to_utf_arr, "messenger"), True)
        self.assertEqual(self.find_result(to_utf_arr, "orangutan"), False)

    def testEntrySearchResults(self):
        url = '/users/search?search=some'
        response = self.client.get(url,
            content_type='application/json')
        to_utf_arr = response.data.decode("utf-8").split()
        self.assertEqual(self.find_result( to_utf_arr, "some"), True)
        self.assertEqual(self.find_result(to_utf_arr, "orangutan"), False)

    def testMultipleSearchResults(self):
        url = '/users/search?search=some+Mark+messenger+Facebook'
        response = self.client.get(url,
            content_type='application/json')
        to_utf_arr = response.data.decode("utf-8").split()
        self.assertEqual(self.find_multiple_results(to_utf_arr, "Mark", "Facebook", "messenger", "some"), True)
        self.assertEqual(self.find_multiple_results(to_utf_arr, "Mark", "Facebook", "messenger", "some", "orangutan"), False)

    def testMultipleCompanySearchResults(self):
        url = '/users/search?search=Oracle+Facebook'
        response = self.client.get(url,
            content_type='application/json')
        to_utf_arr = response.data.decode("utf-8").split()
        self.assertEqual(self.find_multiple_results(to_utf_arr, "Oracle", "Facebook"), True)
        self.assertEqual(self.find_multiple_results(to_utf_arr, "Oracle", "Facebook", "orangutan"), False)

    def testMultiplePersonSearchResults(self):
        url = '/users/search?search=Mark+Gates'
        response = self.client.get(url,
            content_type='application/json')
        to_utf_arr = response.data.decode("utf-8").split()
        self.assertEqual(self.find_multiple_results(to_utf_arr, "Mark", "Gates"), True)
        self.assertEqual(self.find_multiple_results(to_utf_arr, "Mark", "Gates", "orangutan"), False)

    def find_result(self, arr, term):
        count = 0
        for val in arr:
            if val.find(term) > -1:
                count= count + 1
        return count > 4

    def find_multiple_results(self, arr, *args):
        for arg in args:
            count = 0
            for val in arr:
                if val.find(arg) > -1:
                    count = count + 1
            if count <= 4:
                return False
        return True

if __name__ == '__main__':
    unittest.main()
