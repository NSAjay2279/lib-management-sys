import unittest
from app import app


class TestLibraryAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.token = {"Authorization": "secure-token"}

    def test_add_book(self):
        response = self.client.post(
            "/books",
            json={"title": "Book Title", "author": "Author Name"},
            headers=self.token
        )
        self.assertEqual(response.status_code, 201)

    def test_get_books(self):
        response = self.client.get("/books/1", headers=self.token)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
