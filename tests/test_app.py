"""Test cases for frontend."""

import pytest

from maps import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestApp:

    def setUp(self):
        pass

    def test_index(self):
        response = app.test_client().get('/')
        assert response.status_code == 200

    def test_about(self):
        response = app.test_client().get("/about/")
        assert response.status_code == 200
        # assert template.name == "base.html"
        # assert response.data.decode('utf-8') == 'Testing, Flask!'
