import unittest
from app import create_app


class TestAll(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')

    def test_login_status_200(self):
        request, response = self.app.test_client.get('/login')
        assert response.status == 200

    def test_login_put_error(self):
        request, response = self.app.test_client.put('/login')
        assert response.status == 405

if __name__ == '__main__':
    unittest.main()
