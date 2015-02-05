
from __future__ import absolute_import, print_function

from . import cmd_helpers
from . import rest
from . import scheduler
from . import state
from . import election

import time

parser = cmd_helpers.parser(
    description=""
)

parser.add("--port", env_var="PORT", type=int,
           default=7070)
parser.add("--master", env_var="MASTER",
           default="127.0.1.1:5050")
# TODO Is there a way to find "the" zookeeper from the master?
parser.add("--zookeeper", env_var="ZOOKEEPER",
           default="127.0.1.1:2181")
parser.add("--user", env_var="USER",
           default="")
parser.add("--queue-dir", env_var="QUEUE_DIR",
           default="/var/spool/dispatch")


@cmd_helpers.init(parser)
def main():
    elector = election.MasterElection()

    def run_master():
        state.CURRENT = state.State()
        scheduler.CURRENT = scheduler.DispatchScheduler()

        scheduler.CURRENT.run()
        rest.server.run(
            debug=state.ARGS.debug,
            host='0.0.0.0',
            port=state.ARGS.port
        )

    elector.start_election(run_master)

    # TODO - quick-and-dirty - need something better here for the main loop
    while True:
        time.sleep(10)
