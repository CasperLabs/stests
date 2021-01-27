import argparse
import subprocess

from stests import chain
from stests.core import crypto
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from arg_utils import get_network_node
from stests.core.types.infra import Node

# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays an on-chain account balance.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: node index.
ARGS.add_argument(
    "--node",
    default=1,
    dest="node",
    help="Node index, e.g. 1.",
    type=args_validator.validate_node_index
    )

# CLI argument: systemctl command.
ARGS.add_argument(
    "--command",
    dest="command",
    help="systemctl command to run on node, e.g. stop, start, restart.",
    type=str,
    choices=('restart', 'start', 'stop'),
    )

# CLI argument: SSH username.
ARGS.add_argument(
    "--ssh-user",
    default='cladmin',
    dest="ssh_user",
    help="SSH username.",
    type=str,
    )

def remote_node_systemctl(node: Node, ssh_user: str, command: str):
    '''Issue a systemctl command to a remote casper-node instance. This is a
    building block for being able to simulate bringing up/down a casper-node in
    a long-running network.

    This assumes that the given user's keys are installed on both this stests
    control machine as well as on the remote machine to connect to. The given
    user will also need to have sudo access on the remote machine.

    :param node: The Node to run the command on.
    :param ssh_user: The username to SSH into the remote machine as.
    :param command: The `systemctl` command to run on the casper-node service.

    :returns None
    '''

    args = (
        'ssh',
        f'{ssh_user}@{node.host}',
        '-i', '~/aws-casperlabs-marklemoine.pem' # Just for testing
        f'sudo systemctl {command} casper-node.service',
    )

    subprocess.run(args, check=True)

# TODO: Just for testing, remove.
if __name__ == '__main__':
    pass
