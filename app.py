from flask import Flask, render_template, request, redirect, url_for
from mongokit import *
from flask import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_wtf.csrf import CsrfProtect

from flask.ext import admin
from forms import newAttorneyForm, newHonorForm
from models import *

app = Flask(__name__)
CsrfProtect(app)

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
		form.populate_obj(attorney)
		# todo: check to see if the organization name exists in the json file and, if not, to append it to the list
		atty = connection.Attorney.find_and_modify({'_id':ObjectId(attorney_id)}, update={'$set': attorney}, upsert=True, new=True)
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

@app.route('/api/attorneys', methods=["GET"])
def attorneys():
	attorneys = connection.Attorney.find()
	return dumps(attorneys)

@app.route('/api/organizations', methods=["GET"])
def organizations():
	return dumps(json.load(open('data/organizations.json', 'r')))

# Admin Pages
from wtforms import form, fields
from flask.ext.admin.form import Select2Widget
from flask.ext.admin.contrib.pymongo import ModelView, filters
from flask.ext.admin.model.fields import InlineFormField, InlineFieldList
import md5

# User admin
class UserForm(form.Form):
    name = fields.TextField('Name')
    email = fields.TextField('Email')
    usertype = fields.SelectField(choices=[('superuser','superuser'),('admin','admin'),('firmuser','firmuser')], default="firmuser")
    password = fields.PasswordField('Password')

class UserView(ModelView):
    column_list = ('name', 'usertype', 'email', 'password')
    # unicode(md5.new('password').hexdigest())	
    column_sortable_list = ('name', 'usertype', 'email', 'password')

    form = UserForm

app.secret_key = 'test'

if __name__ == "__main__":
    app.debug = True
    admin = admin.Admin(app, name='Honor Roll')
    admin.add_view(UserView(connection.honorroll.user, 'User'))
    app.run()
