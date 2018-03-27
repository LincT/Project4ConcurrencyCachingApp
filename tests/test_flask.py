from project.main import app
import unittest

class FlaskTests(unittest.TestCase):

    def setUp(self):
        #creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_status_code(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertTrue(b'Please search an artist or song' in response.data)

    def test_correct_search(self):
        response = self.app.post('/login', data=dict(search="Britney Spears"))
        self.assertIn(b'Search: Britney Spears', response.data)

    def test_lyric_error_msg(self):
        response = self.app.post('/login', data=dict(search="Katy Perry"))
        self.assertIn(b'Error finding lyrics', response.data)


if __name__ == '__main__':
    unittest.main()