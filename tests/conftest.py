import pytest
from app.app import create_app


@pytest.fixture(scope='session')
def app(request):
    return create_app()


@pytest.fixture(scope='session')
def client(app):
    """Creates a flask.Flask test_client object
    :app: fixture that provided the flask.Flask app
    :returns: flask.Flask test_client object
    """

    return app.test_client()
