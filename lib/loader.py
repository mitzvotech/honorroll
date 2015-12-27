from models import Attorney, Organization
from bson import json_util
import json
from mongoengine import connect
from titlecase import titlecase
import pdb

connect("honorroll-env", host="mongodb://localhost/honorroll-env")


class Loader:
    def __init__(self):
        self.attorneys = self.loadAttorneys()

    def loadAttorneys(self):
        with open('data/attorneys.json', 'r') as f:
            out = json.load(f)
        return out

    def clean_up(self, name):
        if name and type(name) is not dict:
            return titlecase(name).strip()
        else:
            return name

    def insertAttorneys(self):
        """Insert attorneys one-by-one
        """
        out = []
        for a in self.attorneys:
            try:
                org = Organization.objects(
                    organization_name=self.clean_up(a["organization_name"])
                    ).modify(
                        upsert=True, new=True,
                        set__organization_name=self.clean_up(a["organization_name"])
                    ).save()
                attorney = Attorney(
                    first_name=self.clean_up(a["first_name"]),
                    last_name=self.clean_up(a["last_name"]),
                    email_address=self.clean_up(a["email_address"]),
                    organization_name=org.organization_name,
                    records=a["records"]
                ).save()
                out.append(json_util.dumps(attorney))
            except:
                print(a)
                Attorney.drop_collection()
                Organization.drop_collection()
                raise
        return out

if __name__ == "__main__":
    print(len(Loader().insertAttorneys()))
