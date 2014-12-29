from models import *
import json

for organization in connection.Organization.find():
	organization.delete()

f = open('data/organizations.json','r')
d = json.load(f)
for org in d:
	organization = connection.Organization()
	organization["organization_name"] = org
	organization.save()
	print org + ' added!'
