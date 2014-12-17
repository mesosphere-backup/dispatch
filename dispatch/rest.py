
from __future__ import absolute_import, print_function

from flask import Flask
from flask import request

from . import job
from . import scheduler
from .state import CURRENT as STATE

server = Flask(__name__)


@server.route("/run", methods=["POST"])
def run_job():
    current = job.Job(request.get_data())
    STATE.add(current)
    return current.id

@server.route("/job/<id>/data", methods=["GET"])
def get_script(id):
    current = STATE.get(id, None)
    if not current:
        return "", 404

    return current.data
