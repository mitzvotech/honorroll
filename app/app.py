from flask import (
    Flask, render_template
)
from flask_wtf.csrf import CsrfProtect
import os
from models import *


def create_app(config_name='default'):
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', '123456')
    configure_blueprints(app)
    return app


def configure_blueprints(app):
    """Configure application blueprints."""
    from frontend.views import frontend
    from api.views import api
    app.register_blueprint(frontend)
    app.register_blueprint(api, url_prefix='/api')

    return None

app = create_app()

MONGODB_URI = os.environ.get("MONGOLAB_URI", 'mongodb://localhost/honorroll')
MONGODB_DB = os.environ.get("MONGOLAB_DB", 'honorroll')
mongo_client = connect(host=MONGODB_URI)
db = mongo_client[MONGODB_DB]

CsrfProtect(app)
# sslify = SSLify(app)

###
# Defined Routes
###






port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.debug = os.environ.get('ENV_DEBUG', False)
    app.run(host='0.0.0.0', port=port)
