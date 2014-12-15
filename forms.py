from flask_wtf import Form
from wtforms import StringField, HiddenField, SelectField, PasswordField, RadioField, FileField, FieldList, FormField, validators
from datetime import datetime
from flask.ext.admin.model.fields import InlineFormField, InlineFieldList

class newAttorneyForm(Form):
    first_name = StringField(u'First Name', [validators.required()])
    middle_initial = StringField(u'Middle Initial', [validators.optional()])
    last_name = StringField(u'Last Name', [validators.required()])
    email_address = StringField(u'Email Address', [validators.Email(), validators.required()])
    organization_name = StringField(u'Organization', [validators.required()])

class newHonorForm(Form):
	year = StringField(u'Year', [validators.required()], default=datetime.now().year)
	honor_choice = RadioField(u'', choices=[('Honors','More than 50 hours of pro bono'),('High Honors','More than 100 hours of pro bono')])
	rule_49_choice = SelectField(u'Rule 49', choices=[('dc', 'Licensed to practice in DC'), ('49', 'Something Else')])
	date_modified = HiddenField(default=datetime.now)

class AdminAttorneyForm(Form):
    first_name = StringField(u'First Name', [validators.required()])
    middle_initial = StringField(u'Middle Initial', [validators.optional()])
    last_name = StringField(u'Last Name', [validators.required()])
    email_address = StringField(u'Email Address', [validators.Email(), validators.required()])
    organization_name = StringField(u'Organization', [validators.required()])
    records = InlineFieldList(InlineFormField(newHonorForm))

class LoginForm(Form):
    username = StringField(u'Username', [validators.required()])
    password = PasswordField(u'Password', [validators.required()])

class RegisterForm(Form):
    uid = StringField(u'Username', [validators.required()])
    email_address = StringField(u'email_address', [validators.required()])
    password = PasswordField(u'Password', [validators.required()])

class BulkForm(Form):
    f = FileField('Upload the .csv file')