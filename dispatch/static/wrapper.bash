#!/bin/bash

PIPE=remote_pipe
PROGRAM="/bin/bash data"

env
mkfifo $PIPE
nc -l -p $PORT < $PIPE  | $PROGRAM > $PIPE
