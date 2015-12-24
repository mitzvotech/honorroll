from flask import (
    Flask
)
from flask_wtf.csrf import CsrfProtect
from cache import cache

import os
from models import *


def create_app(config_name='default'):
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', '123456')

    # Initalizes the Cache
    cache.init_app(app)

    # Configure the Routes
    configure_blueprints(app)

    MONGODB_URI = os.environ.get(
        "MONGOLAB_URI", 'mongodb://localhost/honorroll')
    MONGODB_DB = os.environ.get("MONGOLAB_DB", 'honorroll')
    mongo_client = connect(host=MONGODB_URI)
    db = mongo_client[MONGODB_DB]

    if os.environ.get("AWS", False):
        set_up_logging()

    return app


def set_up_logging():
    import logging
    import socket
    from logging.handlers import SysLogHandler

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    syslog = SysLogHandler(address=(
        os.environ.get("PAPERTRAIL_HOST"),
        int(os.environ.get("PAPERTRAIL_PORT")),
    ))
    formatter = logging.Formatter('Honor Roll: %(message)s')

    syslog.setFormatter(formatter)
    logger.addHandler(syslog)


def configure_blueprints(app):
    """Configure application blueprints."""
    from frontend.views import frontend
    from api.views import api
    app.register_blueprint(frontend)
    app.register_blueprint(api, url_prefix='/api')

    return None

app = create_app()

CsrfProtect(app)

port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.debug = os.environ.get('ENV_DEBUG', False)
    app.run(host='0.0.0.0', port=port)
