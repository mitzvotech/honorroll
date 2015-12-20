from flask_wtf import Form
from wtforms import (
    StringField, HiddenField, SelectField, PasswordField, RadioField,
    FileField, FieldList, FormField, validators
)
from datetime import datetime
from flask.ext.admin.model.fields import InlineFormField, InlineFieldList
from flask.ext.mongoengine.wtf import model_form
from models import Attorney, Record, Organization


class newAttorneyForm(Form):
    first_name = StringField(
        u'First Name', [validators.InputRequired(message="Required Field")]
    )
    last_name = StringField(
        u'Last Name', [validators.InputRequired(message="Required Field")]
    )
    email_address = StringField(
        u'Email Address',
        [
            validators.Email(),
            validators.InputRequired(message="Required Field")]
    )
    organization_name = StringField(u'Firm/Agency', [validators.Optional()])

choices = [
    ('dc',
        'During the performance of my pro bono work I was a D.C. Bar member.'),
    ('application',
        'During the performance of my pro bono work I was not a D.C. Bar \
        member, but had submitted an application for admission.'),
    ('us', 'During the performance of my pro bono work I was not a D.C. Bar \
        member, but was an employee of the United States.'),
    ('federal',
        'During the performance of my pro bono work I was not a D.C. Bar \
        member, but was a member in good standing of the highest court of any \
        state and provided pro bono legal services to D.C. residents solely \
        before a U.S. special court, department, or agency.'),
    ('program',
        'During the performance of my pro bono work I was not a D.C. Bar \
        member, but provided legal services to D.C. residents as part of \
        a special program for representation or assistance that was expressly \
        authorized by the D.C. Court of Appeals or Superior Court.')]


# newHonorForm = model_form(Record)

class newHonorForm(Form):
    year = StringField(
        u'Year',
        [validators.InputRequired(message="Required Field")], default="2015"
    )
    honor_choice = RadioField(
        u'Honor Level', [validators.InputRequired(message="Required Field")],
        choices=[
            ('Honors', 'I performed 50 hours or more of pro bono services'),
            ('High Honors', 'I performed 100 hours or more of \
                pro bono services')],
        default="Honors")
    rule_49_choice = RadioField(
        u'Rule 49', [validators.InputRequired(message="Required Field")],
        choices=choices, default='dc'
    )
    date_modified = HiddenField(default=datetime.now)


class EmailEditForm(Form):
    email_address = StringField(
        u'Email Address', [
            validators.InputRequired(message="Required Field"),
            validators.Email()
        ])
