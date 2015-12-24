from flask import (
    Blueprint, render_template
)
from bson.json_util import dumps
from models import Attorney, Organization

api = Blueprint('api', __name__, static_folder='../static')


@api.route('/attorneys', methods=["GET"])
def attorneys():
    return Attorney.objects.get_attorneys()


@api.route('/organizations', methods=["GET"])
def organizations():
    return dumps(Organization.dump_list())
