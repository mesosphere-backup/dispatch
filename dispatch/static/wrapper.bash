#!/bin/bash

mkdir .ssh

echo "AuthorizedKeysFile $PWD/.ssh/authorized_keys" >> sshd_config
echo "HostKey $PWD/.ssh/host_key" >> sshd_config
echo "ForceCommand bash $PWD/script" >> sshd_config

cp public_key .ssh/authorized_keys

ssh-keygen -f .ssh/host_key -t rsa -N ''

# NOTE sshd in debug mode doesn't fork a daemon so only one connection is accepted
# before sshd exits -- this is the behavior we want but has the unfortunate
# side-effect of making the client print the bash environment before executing
# the script
/usr/sbin/sshd -p $PORT -f sshd_config -d
