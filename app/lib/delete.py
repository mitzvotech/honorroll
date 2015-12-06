from mongokit import *
from bson.json_util import dumps
from bson.objectid import ObjectId
import json

connection = Connection()
with open('deletes.json','r') as f:
	dels = json.load(f)
for d in dels:
	a = connection.hr.attorneys.remove({"_id":ObjectId(d)})