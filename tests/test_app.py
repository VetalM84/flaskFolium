"""Test cases for frontend."""

import unittest
from datetime import date

from flask import current_app

from maps import create_app, db

from maps.routes import to_date


class BasicsTestCase(unittest.TestCase):
    """General test cases."""

    def setUp(self):
        """Execute before unit test. Create an app and in memory DB."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        """Execute after unit test. Drop DB, session, app."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """Check if it is possible to create an app instance."""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """Check if environment is set to TESTING == True."""
        self.assertTrue(current_app.config["TESTING"])

    def test_index_page(self):
        """Test index page. Check content and status code."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Добавить место вручения" in response.get_data(as_text=True))

    def test_index_with_date_page(self):
        """Test index page with argument named 'date'."""
        response = self.client.get("/?date=2022-08-20")
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        """Test about page. Check content and status code."""
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("О проекте" in response.get_data(as_text=True))

    def test_page_not_found(self):
        """Test 404 response."""
        response = self.client.get("/page_not_found/")
        self.assertEqual(response.status_code, 404)

    def test_success_post_marker(self):
        """POST a new marker. Check flash message and status code."""
        response = self.client.post(
            "/",
            data={
                "coordinates": "50.2202,30.3902",
                "color": "red",
                "comment": "Some test comment",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Точка добавлена!" in response.get_data(as_text=True))

    def test_success_to_date(self):
        """Success test func to convert string from url argument named 'date' to date object."""
        result = to_date("2022-08-20")
        self.assertIsInstance(obj=result, cls=date)

    def test_fail_to_date(self):
        """Fails test func to convert string from url argument named 'date' to date object."""
        with self.assertRaises(ValueError):
            to_date("2022.08.20")
