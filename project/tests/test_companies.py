from flask_testing import TestCase
import unittest
from project.models import Company, User
from project import app, db

class BaseTestCase(TestCase):
    def _login_user(self,email,password,follow_redirects=False):
        return self.client.post('/users/login', 
            data=dict(email=email, 
            password=password), follow_redirects=follow_redirects)

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        user1 = User('aricliesenfelt@gmail.com', 'Aric Liesenfelt', 'password1', '9515706209', True, False)
        user2 = User('tommyhopkins@gmail.com', 'Tommy Hopkins', 'password2', '1111111111', True, True)  
        c1 = Company(name='Intel',description='Computer Chip Maker',
            url='intel.com',logo_url=None,partner_lead='Some guy',
            ops_lead='some other guy',source='no where',round='B',archived=False)
        c2 = Company(name='AMD',description='Yet Another Computer Chip Maker',
            url='7.com',logo_url=None,partner_lead='Some guy',
            ops_lead='some other guy',source='no where',round='Angel',archived=False)        
        db.session.add_all([c1,c2,user1,user2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Should create a new company, redirect to index, and add to the db
    def testCreateNewCompany(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.post('/companies/',
            data = dict(
                name='New Company',
                description='A new company',
                url='www.new.com',
                logo_url='cooolllogo.com',
                partner_lead='Bob Jones',
                ops_lead='Billy Bob',
                source='1',
                round='Angel'
                ), follow_redirects = True
            )

        self.assertEqual(len(Company.query.all()), 3)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('companies/index.html')

    # Should correctly edit user, and return to show page, handle empty
    # form fields (sent as empty strings)
    def testEditCompany(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.post('/companies/2?_method=PATCH',
            data = dict(
                name = 'Not Intel anymore',
                description = 'A changed name',
                url='a new url',
                logo_url="None",
                partner_lead='Big Shot',
                ops_lead='another big shot',
                source='',
                round=""
                ), follow_redirects=True
            )

        self.assertEqual(len(Company.query.all()), 2)
        self.assertEqual(Company.query.get(2).url, 'a new url')
        self.assert_template_used('companies/show.html')
        self.assertEqual(response.status_code, 200)

    # Should allow a user profile to be archived; name must be sent
    # due to validater (will normally prepopulate in form)
    def testArchiveCompany(self):
        self._login_user('tommyhopkins@gmail.com','password2')
        response = self.client.post('/companies/2?_method=PATCH',
            data = dict(
                name = 'OnePlus',
                description = '',
                url='',
                logo_url="",
                partner_lead='',
                ops_lead='',
                source='',
                round="",
                archived=True
                ), follow_redirects=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Company.query.get(2).archived)
        self.assert_template_used('companies/show.html')

if __name__ == '__main__':
    unittest.main()
