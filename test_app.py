import unittest
import json
from app import app


class LibraryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_create_book(self):
        response = self.app.post(
            '/books', json={'title': 'Test Book', 'author': 'Author'})
        self.assertEqual(response.status_code, 201)

# Add more tests for other endpoints...


if __name__ == '__main__':
    unittest.main()
