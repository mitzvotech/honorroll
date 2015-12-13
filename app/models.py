from mongoengine import *


class Record(EmbeddedDocument):
    year = StringField(default="2015")
    honor_choice = StringField()
    rule_49_choice = StringField()
    date_modified = StringField()
    method_added = StringField()


class Organization(Document):
    organization_name = StringField(required=True)

    meta = {
        'collection': 'organizations'
    }

    @queryset_manager
    def dump_list(doc_cls, queryset):
        return queryset.values_list('organization_name')\
                        .order_by('organization_name')


class Attorney(Document):
    first_name = StringField(required=True)
    middle_initial = StringField(required=False)
    last_name = StringField(required=True)
    email_address = EmailField(required=True)
    # records = ListField(Record, required=False)
    records = ListField(DictField())
    organization_name = ReferenceField(Organization)

    meta = {
        'collection': 'attorneys'
    }

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
