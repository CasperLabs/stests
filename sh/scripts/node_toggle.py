import argparse
import itertools as it
import random
from pathlib import Path

from sh.scripts.arg_utils import get_network
from sh.scripts.svc_utils import get_healthy_and_down_nodes
from sh.scripts.svc_utils import remote_node_systemctl
from sh.scripts.svc_utils import SvcCommand
from stests.core.utils import cli as utils
from stests.core.types.infra.enums import NodeStatus
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from stests.core.types.infra.enums import NodeStatus

SVC_COMMAND = SvcCommand.STOP

def get_arg_parser() -> argparse.ArgumentParser:
    # CLI argument parser.
    parser = argparse.ArgumentParser(
        f"Toggles casper-node on a random node from down to up, or vice versa."
    )

    # CLI argument: network name.
    parser.add_argument(
        "--net",
        default=env.get_network_name(),
        dest="network",
        help="Network name {type}{id}, e.g. nctl1.",
        type=args_validator.validate_network,
    )

    # CLI argument: SSH username.
    parser.add_argument(
        "--ssh-user",
        default='cladmin',
        dest="ssh_user",
        help="SSH username.",
        type=str,
    )

    # CLI argument: SSH username.
    parser.add_argument(
        "--ssh-key-path",
        default=None,
        dest="ssh_key_path",
        help="Path to SSH key.",
        type=Path,
    )

    # CLI argument: force flag.
    parser.add_argument(
        "--force",
        action="store_true",
        dest="force",
        help="Run command despite the current status of the node.",
    )

    return parser

def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    network = get_network(args)

    healthy_nodes, down_nodes = get_healthy_and_down_nodes(network)

    # Check that there are enough nodes.
    if not len(healthy_nodes) and not len(down_nodes):
        utils.log('No nodes found, returning')
        return

    # TODO: Do we need to ensure at least one healthy node is always remaining?
    target_node = random.choice(healthy_nodes + down_nodes)
    utils.log(f'Selected node #{target_node.index} for toggling')
    utils.log(f'Current status of node: {target_node.status}')

    if target_node.status is NodeStatus.DOWN:
        # Start the node.
        command = SvcCommand.START
    else:
        # Stop the node.
        command = SvcCommand.STOP

    remote_node_systemctl(
        node=target_node,
        ssh_user=args.ssh_user,
        command=command,
        ssh_key_path=args.ssh_key_path,
        force=args.force,
    )

if __name__ == '__main__':
    parser = get_arg_parser()
    main(parser.parse_args())
