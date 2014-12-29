from models import *

for attorney in connection.Attorney.find():
	attorney.delete()
