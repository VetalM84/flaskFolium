"""Test cases for frontend."""

import unittest
from datetime import date, datetime

from flask import current_app
from folium import folium

from maps import create_app, db
from maps.models import Report
from maps.routes import (
    to_date,
    parse_coordinates,
    add_marker,
    get_all_markers,
)


class BasicsTestCase(unittest.TestCase):
    """General test cases."""

    def setUp(self):
        """Execute before unit test. Create an app and in memory DB."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.current_map = folium.Map(location=(50.45, 30.52))
        self.client = self.app.test_client(use_cookies=True)

        report = Report(
            latitude=50.45,
            longitude=30.52,
            color="red",
            comment="comment",
            ip="127.0.0.1",
        )
        db.session.add(report)
        db.session.commit()

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
        today = datetime.strftime(datetime.today().date(), "%Y-%m-%d")
        response = self.client.get(f"/?date={today}")
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

    def test_to_date(self):
        """Test success and fails func to convert string from url argument named 'date' to date object."""
        result = to_date("2022-08-20")
        self.assertIsInstance(obj=result, cls=date)

        with self.assertRaises(ValueError):
            to_date("2022.08.20")

    def test_parse_coordinates(self):
        """Test success and fails func to parse coordinates gotten from html form."""
        result = parse_coordinates("51.5505,23.7752")
        self.assertIsInstance(obj=result, cls=tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, (51.5505, 23.7752))

        result = parse_coordinates("lat:51.5505 lng:23.7752")
        self.assertIsInstance(obj=result, cls=tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, (51.5505, 23.7752))

        with current_app.test_request_context():
            with self.assertRaises(ValueError):
                parse_coordinates("1.5505,223.7752")

            with self.assertRaises(IndexError):
                parse_coordinates("51.5505")

    def test_add_marker(self):
        """Test success and fails func to add a marker to the map."""
        try:
            add_marker(
                current_map=self.current_map,
                location=(51.5505, 31.0000),
                color="red",
                popup="test",
                tooltip="test",
            )
        except Exception as e:
            self.fail(f"add_marker() raised exception {e}!")

        with current_app.test_request_context():
            with self.assertRaises(ValueError):
                add_marker(
                    current_map=self.current_map,
                    location=(46.46444,),
                    color="red",
                    popup="test",
                    tooltip="test",
                )

    def test_get_all_markers(self):
        """Test func to retrieve all records from DB filtering by date added."""
        result = get_all_markers(date.today())
        self.assertEqual(len(result), 1)
