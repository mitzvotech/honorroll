from mongokit import *
import datetime
from bson.objectid import ObjectId
import os

#MONGODB_URI = os.environ["MONGOLAB_URI"]
MONGODB_DB = os.environ.get("MONGOLAB_DB",'honorroll')
#connection = Connection(MONGODB_URI)
connection = Connection()
db = connection[MONGODB_DB]
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# register the Attorney document with our current connection
@connection.register
class Attorney(Document):
	__collection__ = 'attorneys'
	__database__ = MONGODB_DB
	structure = {
		'first_name': unicode,
		'middle_initial': unicode,
		'last_name': unicode,
		'email_address': unicode,
		'records': [
			{
				'year': unicode,
				'honor_choice': unicode,
				'rule_49_choice': unicode,
				'date_modified': unicode,
				'method_added': unicode
			}
		],
		'organization_name': unicode
	}
	default_values = {
		'records': []
	}
	validators = {
        # 'first_name': max_length(50),
        # 'email': max_length(120)
    }
	use_dot_notation = True

	def __repr__(self):
		return '%s %s %s (%s)' % (self.first_name, self.middle_initial, self.last_name, self.email_address)

@connection.register
class Organization(Document):
	__collection__ = 'organizations'
	__database__ = MONGODB_DB
	structure = {
		'organization_name': unicode
	}
	use_dot_notation = True

	def __repr__(self):
		return '%s' % (self.organization_name)


connection.register([Attorney, Organization])
