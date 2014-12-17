
from __future__ import absolute_import, print_function

import functools
import logging

import configargparse

from . import state


def init(parser=None):

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            state.ARGS = parser.parse_args() if parser else None

            logging.basicConfig(
                level=getattr(logging, state.ARGS.log_level.upper()),
                filename=state.ARGS.log_file
            )

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def parser(**kwargs):
    parser_inst = configargparse.ArgParser(**kwargs)

    parser_inst.add(
        "--debug", default=False, action="store_true"
    )

    parser_inst.add(
        "--log-level", default="warning"
    )
    parser_inst.add(
        "--log-file", default=None
    )

    return parser_inst
