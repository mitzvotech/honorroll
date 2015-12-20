import pytest
from app.models import Attorney, Organization
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
        assert len(Organization.objects) == 1
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


class TestSeleniumViews:

    def test_index_page(client, live_server, driver):
        index_url = live_server.url() + url_for('frontend.index')
        driver.get(index_url)
        assert "Capital Pro Bono Honor Roll" in driver.title

    def test_add_attorney_selenium(client, live_server, driver):
        url = live_server.url() + url_for('frontend.add')
        driver.get(url)
        assert "Register for the Capital Pro Bono Honor Roll" in \
            driver.find_element_by_id('attorneys-form-header').text
        driver.find_element_by_id("first_name").send_keys("Jane")
        driver.find_element_by_id("last_name").send_keys("Smith")
        driver.find_element_by_id("email_address").send_keys("jane@test.com")
        driver.find_element_by_id("organization_name").send_keys("Test Org")
        driver.find_element_by_name("submit").click()
        assert "Add an Honor for Jane Smith" in \
            driver.find_element_by_id('honor-form-header').text


class TestBulkLoad:

    def test_bulk_load(self):
        from app.utils import load_attorneys_from_csv
        # Check to see if the home page works
        load_attorneys_from_csv('docs/bulkattorneys.csv')
        count = Attorney.objects.count()
        assert count == 4
        assert Attorney.objects.get(
            email_address="tim@yo.com"
        ).first_name == "Tim"
