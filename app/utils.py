import csv
# from models import *
from datetime import datetime
import codecs
import json
from models import Attorney, Organization
from flask_mail import Message


def load_attorneys_from_csv(filename):
    with codecs.open(filename, mode='rb', encoding='utf-8') as csvfile:
        attorneys = [row for row in csv.reader(csvfile.read().splitlines())]
        attorneys.pop(0)
        for attorney in attorneys:
            a = Attorney()
            a.first_name = attorney[0]
            a.middle_initial = attorney[1]
            a.last_name = attorney[2]
            a.email_address = attorney[3]
            a.organization_name = Organization.objects(organization_name=attorney[4]).upsert_one().organization_name
            a.records.append({
                'year': attorney[5],
                'honor_choice': attorney[6],
                'rule_49_choice': attorney[7],
                'date_modified': datetime.now(),
                'method_added': u'bulk'
            })
            a.save()
    return True


def check_new_email(email_address):
    try:
        Attorney.objects.get(email_address=email_address)
        return True
    except Attorney.DoesNotExist:
        return False
