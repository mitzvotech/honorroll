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

choices = [('dc','During the performance of my pro bono work I was a D.C. Bar member.'),('application','During the performance of my pro bono work I was not a D.C. Bar member, but had submitted an application for admission.'), ('us','During the performance of my pro bono work I was not a D.C. Bar member, but was an employee of the United States.'), ('federal','During the performance of my pro bono work I was not a D.C. Bar member, but was a member in good standing of the highest court of any state and provided pro bono legal services to D.C. residents solely before a U.S. special court, department, or agency.'), ('program','During the performance of my pro bono work I was not a D.C. Bar member, but provided legal services to D.C. residents as part of a special program for representation or assistance that was expressly authorized by the D.C. Court of Appeals or Superior Court.')]

class newHonorForm(Form):
    year = StringField(u'Year', [validators.required()], default=datetime.now().year)
    honor_choice = RadioField(u'', choices=[('Honors','I performed 50 hours or more of pro bono services'),('High Honors','I performed 100 hours or more of pro bono services')])
    rule_49_choice = RadioField(u'Rule 49', choices=choices)
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