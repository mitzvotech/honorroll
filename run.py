from app.app import *

if __name__ == "__main__":
    app.debug = os.environ.get('ENV_DEBUG', False)
    admin = admin.Admin(app, name='Honor Roll')
    # admin.add_view(AttorneyView(Attorney._get_collection(), 'Attorneys'))
    # admin.add_view(UserView(User._get_collection(), 'Users'))
    app.run(host='0.0.0.0', port=port)
