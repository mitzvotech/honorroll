import csv
from mongokit import *
from bson.json_util import dumps
import json

connection = Connection()
reader=csv.reader(open('attorneys.csv', 'r'), delimiter=',')

entries = set()
out = []
for row in reader:
    key = (row[0], row[2]) # instead of just the last name
    if key not in entries:
        # writer.writerow(row)
        entries.add(key)
    else:
        a = json.loads(dumps(connection.hr.attorneys.find({"first_name":row[0],"last_name":row[2]})))
        out.append(json.loads(dumps(a)))
print(json.dumps(out, indent=2))
