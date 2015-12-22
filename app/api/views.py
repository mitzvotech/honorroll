from flask import (
    Blueprint, render_template
)
from bson.json_util import dumps
from models import Attorney, Organization

api = Blueprint('api', __name__, static_folder='../static')


# @api.route('/attorneys', methods=["GET"])
# def attorneys():
#     out = []
#     for attorney in Attorney.objects[:100]:
#         try:
#             out.append({
#                 'first_name': attorney["first_name"],
#                 'last_name': attorney["last_name"],
#                 'organization_name': attorney.organization_name.id,
#                 'year': "2014",
#                 'honors': attorney["records"][0]["honor_choice"]
#             })
#         except:
#             print(attorney["records"])
#
#     return dumps(out)


@api.route('/organizations', methods=["GET"])
def organizations():
    return dumps(Organization.dump_list())
