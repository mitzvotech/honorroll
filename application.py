from app.app import *

if __name__ == "__main__":
    app.debug = os.environ.get('ENV_DEBUG', False)
    app.run(host='0.0.0.0', port=port)
