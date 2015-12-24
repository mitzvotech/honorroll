from app.app import app as application
import os

if __name__ == "__main__":
    application.debug = os.environ.get('ENV_DEBUG', False)
    application.run(host='0.0.0.0')

    ADMINS = ['vdavez@gmail.com']
    if not application.debug:
        import logging

        FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
        DATE_FMT = '%m/%d/%Y %H:%M:%S'

        loglevel = logging.DEBUG
        logging.basicConfig(format=FORMAT, datefmt=DATE_FMT, level=loglevel)
