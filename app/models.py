from mongoengine import *
from bson import json_util


class AttorneyQuerySet(QuerySet):

    def get_attorneys(self):
        out = []

        map = """
        function () {
            emit({
                'first_name': this.first_name,
                'last_name': this.last_name,
                'organization_name': this.organization_name.valueOf(),
                'records': this.records
            }, 1)
        }
        """
        mp = self.map_reduce(
            map,
            "function(key, values) { return key }",
            output="inline"
        )
        for x in list(mp):
            out.append(x.key)
        return json_util.dumps(out)

    # def get_attorneys(self):
    #     out = []
    #     for attorney in self:
    #         out.append({
    #             'first_name': attorney.first_name,
    #             'last_name': attorney.last_name,
    #             'organization_name': str(attorney.organization_name),
    #             'records': attorney.records
    #         })
    #     return json_util.dumps(out)


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

    def to_json(self):
        return "%s" % self.organization_name

    def __str__(self):
        return "%s" % self.organization_name


class Attorney(Document):
    first_name = StringField(required=True)
    middle_initial = StringField(required=False)
    last_name = StringField(required=True)
    # TODO: On production, make this required=True, unique=True
    email_address = EmailField(unique=True, sparse=True)
    records = ListField(DictField())
    organization_name = StringField(required=False)

    meta = {
        'collection': 'attorneys',
        'queryset_class': AttorneyQuerySet,
        'strict': False
    }
