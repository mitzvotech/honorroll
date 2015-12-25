from app.app import create_app
from app.models import Attorney, Organization
import datetime
import pytest
import os
from selenium import webdriver


os.environ["MONGOLAB_URI"] = "mongodb://localhost/honorroll"


def base_url(live_server):
    return live_server.url()


@pytest.fixture(scope='session')
def app(request):
    app = create_app()
    app.debug = True
    return app


@pytest.fixture(scope='session')
def driver(request):
    browser = webdriver.PhantomJS('phantomjs')
    browser.set_page_load_timeout(30)
    request.addfinalizer(lambda *args: browser.quit())
    return browser


@pytest.fixture(scope="session")
def add_attorney(request):
    org = Organization(organization_name="TestOrg").save()
    attorney = Attorney(
        first_name="John", last_name="Doe", organization_name=org,
        email_address="john.doe@example.com",
        records=[
            {
                "year": "2015", "honor_choice": "Honors",
                "rule_49_choice": "dc", "method_added": "bulk",
                "date_modified": datetime.datetime.now()
            }
        ]
    ).save()

    def teardown():
        Attorney.objects.delete()
        Organization.objects.delete()

    request.addfinalizer(teardown)
    return add_attorney
