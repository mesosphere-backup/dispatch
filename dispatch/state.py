
from __future__ import absolute_import, print_function

from Queue import Queue
import json
import os
from . import log

ARGS = None

class State(dict):

    def __init__(self):
        self.queue = Queue()
        self.load()

    def add(self, job):
        self._add(job)
        self.store()

    def _add(self, job):
        self[job.id] = job
        self.queue.put(job.id)

    def size(self):
        return self.queue.qsize()

    @property
    def empty(self):
        return self.size() == 0

    def next(self):
        try:
            return self[self.queue.get()]
        finally:
            self.store()

    def store(self):
        if not os.path.exists(ARGS.queue_dir):
            log.info("Making %r", ARGS.queue_dir)
            os.makedirs(ARGS.queue_dir)
        log.info("Writing queue")
        with open(ARGS.queue_dir + '/queue.json', 'w') as conf:
            conf.write(json.dumps([j for j in self.queue.queue]))

    def load(self):
        from . import job
        if not os.path.exists(ARGS.queue_dir + '/queue.json'):
            return
        log.info("Loading queue")
        with open(ARGS.queue_dir + '/queue.json', 'r') as conf:
            for data in json.loads(conf.read()):
                j = job.Job(data['data'])
                for k in ['id', 'location', 'port', 'resource', 'running',
                          'uris']:
                    j.__dict__[k] = data[k]
                self._add(j)

CURRENT = None
