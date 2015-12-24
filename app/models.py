from mongoengine import *
from bson import json_util


class AttorneyQuerySet(QuerySet):
    def get_attorneys(self):
        return self.exclude('id').exclude('email_address').to_json()


class Record(EmbeddedDocument):
    year = StringField(default="2015")
    honor_choice = StringField()
    rule_49_choice = StringField()
    date_modified = StringField()
    method_added = StringField()


class Organization(Document):
    organization_name = StringField(required=True)

    meta = {
        'collection': 'organizations',
        'indexes': ['organization_name']
    }

    @queryset_manager
    def dump_list(doc_cls, queryset):
        return queryset.values_list('organization_name')\
                        .order_by('organization_name')

    def __str__(self):
        return "%s" % self.organization_name


class Attorney(Document):
    first_name = StringField(required=True)
    middle_initial = StringField(required=False)
    last_name = StringField(required=True)
    email_address = EmailField(required=True)
    # records = ListField(Record, required=False)
    records = ListField(DictField())
    organization_name = ReferenceField(Organization)

    meta = {
        'collection': 'attorneys',
        'queryset_class': AttorneyQuerySet,
        'strict': False
    }

    def to_json(self):
        data = self.to_mongo()
        try:
            data["organization_name"] = self.organization_name \
                                            .organization_name
        except:
            data["organization_name"] = ""
        return json_util.dumps(data)
