import os
import unittest
import json

from app import app, db

TEST_DB = 'test.db'


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """Initial test: Ensure flask was set up correctly"""
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        tester = os.path.exists("flaskr.db")
        self.assertTrue(tester)


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test."""
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.drop_all()

    def login(self, username, password):
        """Login Helper Function"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/logout', follow_redirects=True)

    # Assert Functions

    def test_empty_db(self):
        """Ensure database is blank"""
        rv = self.app.get('/')
        assert b'No entries yet. Add some!' in rv.data

    def test_login_logout(self):
        """Test login and logout using helper functions"""
        rv = self.login(
            app.config['USERNAME'],
            app.config['PASSWORD'],
        )
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login(
            app.config['USERNAME'] + 'x',
            app.config['PASSWORD'],
        )
        assert b'Invalid username' in rv.data
        rv = self.login(
            app.config['USERNAME'],
            app.config['PASSWORD'] + 'x',
        )
        assert b'Invalid password' in rv.data

    def test_messages(self):
        """Ensure that a user can post messages."""
        self.login(
            app.config['USERNAME'],
            app.config['PASSWORD']
        )
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

    def test_delete_message(self):
        """Ensure the messages are being deleted"""
        rv = self.app.get('/delete/1')
        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(data['status'], 1)

    def test_search(self):
        """Make sure the search page is displayed"""
        tester = app.test_client(self)
        response = tester.get('/search/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
