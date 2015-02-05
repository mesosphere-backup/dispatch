
from __future__ import absolute_import, print_function

import json

from flask import Flask
from flask import request

from . import job
from . import scheduler
from . import state

server = Flask(__name__)


@server.route("/run", methods=["POST"])
def run_job():
    current = job.Job(request.get_data())
    state.CURRENT.add(current)
    return current.id

@server.route("/job/<id>/data", methods=["GET"])
def get_script(id):
    current = state.CURRENT.get(id, None)
    if not current:
        return "", 404

    return current.data

@server.route("/job/<id>", methods=["GET"])
def get_job(id):
    current = state.CURRENT.get(id, None)
    if not current:
        return "", 404

    return json.dumps({
        "running": current.running,
        "ip": current.location,
        "port": current.port
    })
