from flask import (
    Blueprint, render_template
)
from bson.json_util import dumps
from models import Attorney, Organization
from app.cache import cache

api = Blueprint('api', __name__, static_folder='../static')


@cache.cached(timeout=50)
@api.route('/attorneys', methods=["GET"])
@api.route("/attorneys/<attorney_id>", methods=["GET"])
def attorneys(attorney_id=None):
    if attorney_id is not None:
        return dumps(Attorney.objects(id=attorney_id).first())
    return Attorney.objects.get_attorneys()


@api.route('/organizations', methods=["GET"])
@api.route('/organizations/<organization_id>', methods=["GET"])
def organizations(organization_id=None):
    if organization_id is not None:
        return dumps({
            "organization_name": Organization.objects(id=organization_id)
                                             .first().organization_name
        })
    return dumps(Organization.dump_list())
