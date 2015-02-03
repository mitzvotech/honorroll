from app.app import *

if __name__ == "__main__":
    app.debug = os.environ.get('ENV_DEBUG',False)
    admin = admin.Admin(app, name='Honor Roll')#,base_template="admin.html")
    admin.add_view(AttorneyView(db.attorneys, 'Attorneys'))
    admin.add_view(UserView(db.users, 'Users'))
    app.run(host='0.0.0.0', port=port)