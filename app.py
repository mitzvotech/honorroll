from flask import Flask, render_template, request, redirect, url_for, flash, Markup
from mongokit import *
from flask import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_wtf.csrf import CsrfProtect
import bcrypt
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from pymongo import Connection

from forms import newAttorneyForm, newHonorForm, BulkForm, LoginForm, RegisterForm, AdminAttorneyForm, EmailEditForm
from models import *
from lib.email import send_confirmation
from utils import update_organizations, mail_bulk_csv, check_new_email

app = Flask(__name__)
CsrfProtect(app)

from flask_sslify import SSLify
sslify = SSLify(app)

import mandrill
mandrill_client = mandrill.Mandrill(os.environ.get("SMTP_USER_PWD"))

###
# Defined Routes
###

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/view")
def view():
	attorneys = connection.Attorney.find()
	return render_template("view.html", attorneys=attorneys)

@app.route("/attorneys", methods=["GET", "POST"])
@app.route("/attorneys/<attorney_id>", methods=["GET", "POST"])
def add(attorney_id=None):
    if attorney_id == None:
        attorney = connection.Attorney()
    else:
        attorney = connection.Attorney.find_one({'_id':ObjectId(attorney_id)})
    form = newAttorneyForm(obj=attorney)
    if form.validate_on_submit():
		
        # upsert the attorney information into the database
        form.populate_obj(attorney)
        if attorney_id == None and check_new_email(attorney.email_address):
            flash(Markup("A user with that email address already exists. Please use this edit feature to make changes"))
            return redirect(url_for('email_edit'))
        else:
            atty = connection.Attorney.find_and_modify({'_id':ObjectId(attorney_id)}, update={'$set': attorney}, upsert=True, new=True)

        # check to see if the organization name exists in the json file and, if not, to append it to the list
        update_organizations(form.organization_name.data)

        msg = send_confirmation(atty._id, atty.email_address)
        result = mandrill_client.messages.send(message=msg)
        # go to the honor form to add an honors record
        return redirect(url_for('honor', attorney_id=atty._id))

    return render_template("form.html", form=form)

@app.route("/honor/<attorney_id>", methods=["GET", "POST"])
def honor(attorney_id=None):
	attorney = connection.Attorney.find_one({'_id':ObjectId(attorney_id)})
	form = newHonorForm()
	if form.validate_on_submit():
		# todo: Add a check to see whether the year is already there, and do an upsert instead of an append
		attorney["records"].append(form.data)
		attorney["records"][len(attorney["records"])-1]["method_added"] = u"website"
		attorney.save()
		return redirect(url_for('view'))
	return render_template('honor.html', form=form, attorney=attorney)

@app.route("/email_edit", methods=["GET","POST"])
def email_edit():
    form = EmailEditForm()
    if form.validate_on_submit():
        attorney = connection.Attorney.find_one({"email_address":form.email_address.data})
        if attorney == None:
            flash('No email address found. Please try again.')
            return render_template("email_edit.html", form=form)
        else:
            msg = send_confirmation(attorney._id, attorney.email_address)
            result = mandrill_client.messages.send(message=msg)
            return redirect(url_for('index'))
    return render_template("email_edit.html", form=form)
        

### 
# Upload a CSV of attorneys 
### 

# ToDo: change the template to allow for mail of bulkattorneys.csv
from werkzeug import secure_filename
from utils import load_attorneys_from_csv
@app.route('/upload', methods=["GET","POST"])
def upload():
    form = BulkForm()
    if form.validate_on_submit():
        filename = secure_filename(form.f.data.filename)
        form.f.data.save('uploads/' + filename)
        if load_attorneys_from_csv('uploads/' + filename):
            return redirect('view')
    else:
        filename = None
    return render_template('upload.html', form=form, filename=filename)

@app.route('/api/attorneys', methods=["GET"])
def attorneys():
	attorneys = connection.Attorney.find(fields={"_id":False, "email_address":False})
	return dumps(attorneys)

@app.route('/api/organizations', methods=["GET"])
def organizations():
    organizations = connection.Organization.find(fields={"_id":False})
    out = []
    for org in organizations:
        out.append(org["organization_name"])
    return dumps(sorted(out))

@app.route('/api/users', methods=["GET"])
def users():
	users = db.users.find()
	return dumps(users)

#### 
# User Authentication
####

login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class User(Document):
    def __init__(self, user_id):
        self.id = user_id.lower()
        self.db = db.users
        self.account = self.db.find_one({'uid': self.id})

    def create(self):
        self.db.insert({'uid': self.id})
        self.account = self.db.find_one({'uid': self.id})

    def save(self):
        self.db.save(self.account)

    def password_valid(self, pwd):
        pwd_hash = self.account['password_hash']
        return bcrypt.hashpw(pwd, pwd_hash) == pwd_hash

    # The methods below are required by flask-login
    def is_authenticated(self):
        """Always return true - we don't do any account verification"""
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

@app.route("/register", methods=['GET', 'POST'])
# @login_required
def register():
    opts = {}
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.uid.data)
        if user.account:
            opts['username_exists'] = True
            return render_template('register.html', opts=opts, form=form)
        user.create()
        pwd_hash = bcrypt.hashpw(form.password.data, bcrypt.gensalt())
        user.account['password_hash'] = pwd_hash
        user.account['email_address'] = form.email_address.data
        user.save()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    opts = {}
    form = LoginForm()
    next_page = request.args.get('next')
    if form.validate_on_submit():
        user = User(form.username.data)
        if not user.account or not user.password_valid(form.password.data):
            flash('invalid_username_or_password')
            return render_template('login.html', form=form)
        login_user(user)
        return redirect(next_page or url_for('index'))
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

login_manager.login_view = "login"


###
# Administration Pages
###

from flask.ext import admin
from flask.ext.admin.contrib.pymongo import ModelView

class AttorneyView(ModelView):
    column_list = ('first_name', 'middle_initial', 'last_name','email_address','organization_name')
    column_sortable_list = ('first_name', 'middle_initial', 'last_name','email_address','organization_name')

    form = AdminAttorneyForm

    def is_accessible(self):
        return current_user.is_authenticated()

class UserView(ModelView):
    column_list = ('uid', 'email_address', 'password_hash')
    column_sortable_list = ('uid', 'email_address','password_hash')

    form = RegisterForm

    def is_accessible(self):
        return current_user.is_authenticated()


from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

app.secret_key = os.environ.get('SECRET_KEY')
port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.debug = False
    admin = admin.Admin(app, name='Honor Roll')#,base_template="admin.html")
    admin.add_view(AttorneyView(db.attorneys, 'Attorneys'))
    admin.add_view(UserView(db.users, 'Users'))
    app.run(host='0.0.0.0', port=port)
