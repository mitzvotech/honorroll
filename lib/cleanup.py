from pymongo import MongoClient
import os
from bson import json_util
from numpy import unique

client = MongoClient(os.environ.get("MONGOLAB_URI"))
db = client[os.environ.get("MONGOLAB_DB")]


class Organization:

    def __init__(self):
        self.orgs = self.get_orgs()
        self.count = len(self.orgs)

    def get_orgs(self):
        out = []
        for org in db.organizations.find():
            out.append(org)
        return out

    def get_unique_orgs(self):
        out = []
        for org in self.orgs:
            try:
                out.append(org["organization_name"].strip())
            except:
                pass
        return unique(out)


class Attorney:

    def __init__(self):
        self.attorneys = self.get_attorneys()
        self.count = len(self.attorneys)

    def get_attorneys(self):
        out = []
        for org in db.attorneys.find():
            out.append(org)
        return out

    def get_unique_orgs(self):
        out = []
        for attorney in self.attorneys:
            try:
                out.append(attorney["organization_name"].strip())
            except:
                pass
        return unique(out)


if __name__ == "__main__":
    org = Organization()
    attorney = Attorney()
    print(json_util.dumps(attorney.get_unique_orgs(), indent=2))
