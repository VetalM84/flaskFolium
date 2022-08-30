"""Test cases for frontend."""

import unittest

from flask import current_app

from maps import create_app, db


class BasicsTestCase(unittest.TestCase):
    """General test cases."""

    def setUp(self):
        """Execute before unit test. Create an app and in memory DB."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

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
