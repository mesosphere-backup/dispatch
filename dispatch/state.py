
from __future__ import absolute_import, print_function

from Queue import Queue

ARGS = None

class State(dict):

    def __init__(self):
        self.queue = Queue()

    def add(self, job):
        self[job.id] = job
        self.queue.put(job.id)

    def size(self):
        return self.queue.qsize()

    @property
    def empty(self):
        return self.size() == 0

    def next(self):
        return self[self.queue.get()]

CURRENT = State()
