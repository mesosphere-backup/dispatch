
from __future__ import absolute_import, print_function

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

    def location(self):
        return urlparse.urljoin(
            "http://{0}:{1}".format(
                socket.gethostbyname(socket.gethostname()),
                state.ARGS.port),
            "/job/{0}/data".format(self.id)
        )
