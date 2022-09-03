"""Test cases for API."""

import unittest
from datetime import datetime

from flask import json
from maps import create_app, db
from maps.models import Report


class APITestCase(unittest.TestCase):
    """General API test cases."""

    def setUp(self):
        """Execute before unit test. Create an app and in memory DB."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
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

    def test_doc_page(self):
        """Test documentation page is available."""
        response = self.client.get("/api/v1/doc/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("swagger.json" in response.get_data(as_text=True))

    def test_get_markers_by_date(self):
        """Test get markers by date. Check content and status code."""
        today = datetime.strftime(datetime.today().date(), "%Y-%m-%d")
        response = self.client.get(f"/api/v1/markers/{today}/")
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(response.status_code, 200)

    def test_put_marker(self):
        """Test PUT marker. Check status code."""
        data = json.dumps(
            {
                "latitude": 51.5505,
                "longitude": 23.7752,
                "color": "red",
                "comment": "string",
            }
        )
        response = self.client.put("/api/v1/markers/", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
