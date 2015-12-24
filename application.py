from app.app import app as application
import os

if __name__ == "__main__":
    application.debug = os.environ.get('ENV_DEBUG', False)
    application.run(host='0.0.0.0')
