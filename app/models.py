from mongoengine import *


class Record(EmbeddedDocument):
    year = StringField(default="2015")
    honor_choice = StringField()
    rule_49_choice = StringField()
    date_modified = StringField()
    method_added = StringField()


class Organization(Document):
    organization_name = StringField(required=True)


class Attorney(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email_address = EmailField(required=True),
    records = ListField(Record)
    organization_name = ReferenceField(Organization)
