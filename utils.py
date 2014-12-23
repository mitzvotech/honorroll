import csv
from models import *
from datetime import datetime
import codecs
import json
from flask_mail import Message

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

def mail_bulk_csv(email_recipient):
    msg = Message("Bulk Upload to Pro Bono Honor Roll",
                  sender="do-not-reply@esq.io",
                  recipients=[email_recipient])
    msg.html = '<p>Thank you for your interest in using the bulk upload feature of the Pro Bono Honor Roll.</p><p>Attached to this email is a template CSV file that you should use to upload the attorney information. (If you have difficulty getting the attachment from this email, you may download a copy at this link: <a href="https://probonohonorroll.herokuapp.com/static/docs/bulkattorneys.csv">https://probonohonorroll.herokuapp.com/static/docs/bulkattorneys.csv</a>)</p> <p>Open the CSV file in Excel or similar spreadsheet application. When you are done, please email the completed CSV file to the following email address: XXXX.</p> <p>If you have any technical difficulties, please email Dave Zvenyach at <a href="mailto:dave@esq.io">dave@esq.io</a>.</p> <p>Thank you so much.</p>'
    with app.open_resource("static/docs/bulkattorneys.csv") as fp:
        msg.attach("bulkattorneys.csv", "text/csv", fp.read())
    return msg

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

def update_organizations(organization_name):
    f = open('data/organizations.json', 'r+')
    data = json.load(f)
    if organization_name not in data:
        data.append(organization_name)
        out = json.dumps(sorted(data))
        f.seek(0)
        f.write(out)
    f.close()
    return True