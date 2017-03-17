from flask_testing import TestCase
import unittest
from project.models import Company
from project import app, db

class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        c1 = Company(name='App Academy',description='Another Bootcamp',
            url='galvanize.com',logo_url=None,partner_lead='Some guy',
            ops_lead='some other guy',source='no where',round='B',archived=False)
        c2 = Company(name='Hack Reactor',description='Yet Another Bootcamp',
            url='7.com',logo_url=None,partner_lead='Some guy',
            ops_lead='some other guy',source='no where',round='Angel',archived=False)        
        db.session.add_all([c1,c2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Should create a new company, redirect to index, and add to the db
    def testCreateNewCompany(self):
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
        response = self.client.post('/companies/2?_method=PATCH',
            data = dict(
                name = 'Not Hack Reactor anymore',
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
        self.assertEqual(Company.query.get(2).name, 'Not Hack Reactor anymore')
        self.assert_template_used('companies/show.html')
        self.assertEqual(response.status_code, 200)

    # Should allow a user profile to be archived; name must be sent
    # due to validater (will normally prepopulate in form)
    def testArchiveCompany(self):
        response = self.client.post('/companies/2?_method=PATCH',
            data = dict(
                name = 'Hack Rector',
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
