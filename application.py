from app.app import app as application
import os

if __name__ == "__main__":
    application.debug = os.environ.get('ENV_DEBUG', False)
    application.run(host='0.0.0.0')

    ADMINS = ['vdavez@gmail.com']
    if not application.debug:
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1',
                                   'capitalprobono@esq.io',
                                   ADMINS, 'YourApplication Failed')
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
