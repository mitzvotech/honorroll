import csv
from models import *
from datetime import datetime
import codecs

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def load_attorneys_from_csv(filename):
    with codecs.open(filename, mode='rb', encoding='utf-8') as csvfile:
        attorneys = [row for row in csv.reader(csvfile.read().splitlines())]
        attorneys.pop(0)
        for attorney in attorneys:
            a = connection.Attorney()
            a['first_name'] = unicode(attorney[0])
            a['middle_initial'] = unicode(attorney[1])
            a['last_name'] = unicode(attorney[2])
            a['email_address'] = unicode(attorney[3])
            a['organization_name'] = unicode(attorney[4])
            record = {
                'year': unicode(attorney[5]),
                'honor_choice': unicode(attorney[6]),
                'rule_49_choice': unicode(attorney[7]),
                'date_modified': unicode(datetime.now()),
                'method_added': u'bulk'
            }
            a['records'].append(record)
            print a 
            a.save()
            print "User Added"
    return True