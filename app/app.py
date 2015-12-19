from flask import (
    Flask, render_template, request, redirect, url_for, flash, Markup, json
)
from bson.objectid import ObjectId
from flask_wtf.csrf import CsrfProtect
import os

from forms import (
    newAttorneyForm, newHonorForm, EmailEditForm
)
from models import *
from lib.email import send_confirmation
from utils import update_organizations, check_new_email
# from flask_sslify import SSLify
import mandrill

from flask.ext.admin.contrib.pymongo import ModelView
from flask.ext.mongoengine.wtf import model_form

# from werkzeug.contrib.fixers import ProxyFix


def create_app(config_name='default'):
    app = Flask(__name__)
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

mandrill_client = mandrill.Mandrill(os.environ.get("SMTP_USER_PWD", ""))

###
# Defined Routes
###


@app.route("/attorneys", methods=["GET", "POST"])
@app.route("/attorneys/<attorney_id>", methods=["GET", "POST"])
def add(attorney_id=None):
    if attorney_id is None:
        attorney = Attorney()
    else:
        attorney = Attorney.objects.get(id=ObjectId(attorney_id))

    form = newAttorneyForm(obj=attorney)
    form.populate_obj(attorney)
    if form.validate_on_submit():

        # upsert the attorney information into the database
        form.populate_obj(attorney)
        if attorney_id is None and check_new_email(attorney["email_address"]):
            flash(Markup("A user with that email address already exists. \
                          Please use this edit feature to make changes"))
            return redirect(url_for('email_edit'))
        else:
            attorney["organization_name"] = Organization.objects.modify(
                organization_name=form.organization_name.data, upsert=True
            )
            atty = attorney.save()

        # check to see if the organization name exists in the json file and,
        # if not, to append it to the list
        atty_id = str(atty.id)
        # check to see if the user is coming from the email.
        if attorney_id is not None:
            # Assuming you know the url, don't send a confirmation email
            return redirect(
                url_for('honor', attorney_id=atty_id)
            )
        else:
            # But if you *don't* know the url, send a confirmation email
            msg = send_confirmation(atty_id, atty.email_address)
            result = mandrill_client.messages.send(message=msg)

        # go to the honor form to add an honors record
        return redirect(url_for('honor', attorney_id=atty_id))
    return render_template("form.html", form=form)


@app.route("/honor/<attorney_id>", methods=["GET", "POST"])
def honor(attorney_id=None):
    attorney = Attorney.objects.get(id=ObjectId(attorney_id))
    form = newHonorForm()
    if form.validate_on_submit():
        # todo: Add a check to see whether the year is already there,
        # and do an upsert instead of an append
        records = attorney["records"]
        for rec in records:
            if form.year.data == rec['year']:
                records.remove(rec)
        records.append(form.data)
        attorney["records"] = records
        attorney["records"][len(attorney["records"])-1]["method_added"] = \
            u"website"
        attorney.save()
        return redirect(url_for('frontend.thanks'))
    return render_template('honor.html', form=form, attorney=attorney)


@app.route("/email_edit", methods=["GET", "POST"])
def email_edit():
    form = EmailEditForm()
    if form.validate_on_submit():
        attorney = db.attorneys.find_one(
            {"email_address": form.email_address.data}
        )
        if attorney is None:
            flash('No email address found. Please try again.')
            return render_template("email_edit.html", form=form)
        else:
            atty_id = str(attorney["_id"])
            msg = send_confirmation(atty_id, attorney["email_address"])
            result = mandrill_client.messages.send(message=msg)
            return redirect(url_for('frontend.index'))
    return render_template("email_edit.html", form=form)


app.secret_key = os.environ.get('SECRET_KEY', '123456')
port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.debug = os.environ.get('ENV_DEBUG', False)
    app.run(host='0.0.0.0', port=port)
