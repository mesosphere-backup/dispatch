
from __future__ import absolute_import, print_function

from . import cmd_helpers
from . import rest
from . import scheduler
from . import state

parser = cmd_helpers.parser(
    description=""
)

parser.add("--port", env_var="PORT", type=int,
    default=7070)
parser.add("--master", env_var="MASTER",
    default="127.0.1.1:5050")
parser.add("--user", env_var="USER",
    default="")

@cmd_helpers.init(parser)
def main():
    scheduler.CURRENT = scheduler.DispatchScheduler()

    scheduler.CURRENT.run()
    rest.server.run(
        debug=state.ARGS.debug,
        host='0.0.0.0',
        port=state.ARGS.port
    )
