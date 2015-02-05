from __future__ import absolute_import, print_function

from kazoo.client import KazooClient
import os.path
import threading

from . import log
from . import state

ELECTION_PATH = '/dispatch/election'


class MasterElection(object):
    def __init__(self):
        self.zk = KazooClient(hosts=state.ARGS.zookeeper)
        self.master_notified = False
        self.my_node = None
        self.zk.start()  # Stop never called
        self.zk.ensure_path(ELECTION_PATH)

    def start_election(self, master_callback):
        """
        Start the master election.

        If this node is the master, the callback will be called once.

        :params master_callback: Called if this node is the master
        """
        self.callback = master_callback
        self.my_node = self.zk.create(ELECTION_PATH + '/n_',
                                      ephemeral=True, sequence=True)
        self.zk.get_children(ELECTION_PATH, watch=self._election_update)
        self._election_update()

    def _election_update(self, data=None):
        def worker():
            try:
                self.master_notified = True
                self.callback()
            except Exception as e:
                self.master_notified = False
                log.info("Failed to activate master, redoing election: %r", e)
                self.zk.delete(self.my_node)
                self.my_node = self.zk.create(ELECTION_PATH + '/n_',
                                              ephemeral=True, sequence=True)
                self._election_update()

        if not self.master_notified and \
                sorted(self.zk.get_children(ELECTION_PATH))[0] == \
                os.path.basename(self.my_node):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
