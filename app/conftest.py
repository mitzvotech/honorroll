from app.app import create_app
from app.models import Attorney, Organization
import datetime
import pytest


@pytest.fixture(scope='session')
def app(request):
    return create_app()


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