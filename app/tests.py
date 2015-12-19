import pytest
from app.models import Attorney
from flask import url_for
import json


class TestFrontend:

    def test_frontend_home(self, client):
        # Check to see if the home page works
        res = client.get(url_for('frontend.index'))
        assert "Open Letter to Capital Pro Bono Honor Roll Registrants from Chief Judge Eric T. Washington and Chief Judge Lee F. Satterfield" in str(res.get_data())
        assert res.status_code == 200

    def test_frontend_questions(self, client):
        # Check to see if the home page works
        res = client.get(url_for('frontend.questions'))
        assert res.status_code == 200

    def test_frontend_thanks(self, client):
        # Check to see if the home page works
        res = client.get(url_for('frontend.thanks'))
        assert res.status_code == 200


class TestAPI:

    def test_api_attorneys(self, client):
        # Check to see if the home page works
        res = client.get(url_for('api.attorneys'))
        assert res.status_code == 200

    def test_attorney_organizations(self, client):
        # Check to see if the home page works
        res = client.get(url_for('api.organizations'))
        assert res.status_code == 200


@pytest.mark.usefixtures("add_attorney")
class TestDatabase:
    def test_add_attorney(self):
        assert len(Attorney.objects) == 1

    def test_api_after_add(self, client):
        res = json.loads(
            client.get(url_for('api.attorneys')).get_data().decode('utf-8')
        )
        assert len(res) == 1    # should have one attorney in the api
        assert res[len(res) - 1]["first_name"] == "John"

    def test_frontend_attorneys(self, client):
        # Check to see if the home page works
        res = client.get(url_for('frontend.view'))
        assert " <td>John</td>\n" in res.get_data().decode('utf-8')
