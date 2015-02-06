
from __future__ import absolute_import, print_function

import json
import socket
import urlparse
import uuid

from . import state


class Job(object):

    resource = {
        "cpus": 0.01,
        "mem": 10
    }

    def __init__(self, data):
        self.data = data
        self.id = str(uuid.uuid4())
        self.port = None
        self.location = None
        self.running = False
        self.script, self.public_key = json.loads(self.data)

    def uris(self):
        # XXX - wrapper location shouldn't live here.
        base = "http://{0}:{1}".format(
            socket.gethostbyname(socket.gethostname()),
            state.ARGS.port)
        return [
            urlparse.urljoin(base, "/static/wrapper.bash"),
            urlparse.urljoin(base, "/static/sshd_config"),
            urlparse.urljoin(base, "/job/{0}/script".format(self.id)),
            urlparse.urljoin(base, "/job/{0}/public_key".format(self.id)),
            ]

    def connection(self):
        return "{0}:{1}".format(self.location, self.port)
