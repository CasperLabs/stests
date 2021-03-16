import argparse
import enum
import subprocess
from pathlib import Path

from stests import chain
from stests.core import crypto
from stests.core.cache.ops import infra
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from stests.core.types.infra import Node
from stests.core.types.infra.enums import NodeStatus
from .arg_utils import get_network_node

class SvcCommand(str, enum.Enum):
    STOP = 'stop'
    START = 'start'

def get_healthy_nodes(network):
    nodes = infra.get_nodes(network)
    utils.log(nodes)
    return nodes

def get_arg_parser(command: SvcCommand) -> argparse.ArgumentParser:
    # CLI argument parser.
    parser = argparse.ArgumentParser(
        f"Executes a systemctl '{command}' command to the casper-node service on a node."
    )

    # CLI argument: network name.
    parser.add_argument(
        "--net",
        default=env.get_network_name(),
        dest="network",
        help="Network name {type}{id}, e.g. nctl1.",
        type=args_validator.validate_network,
    )

    # CLI argument: node index.
    parser.add_argument(
        "--node",
        default=1,
        dest="node",
        help="Node index, e.g. 1.",
        type=args_validator.validate_node_index
    )

    # # CLI argument: systemctl command.
    # parser.add_argument(
    #     "--command",
    #     default='status',
    #     dest="command",
    #     help="systemctl command to run on node, e.g. stop, start, restart.",
    #     type=str,
    #     choices=('restart', 'start', 'status', 'stop'),
    # )

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

def remote_node_systemctl(
    node: Node,
    ssh_user: str,
    command: SvcCommand,
    ssh_key_path: Path=None,
    check_rc: bool=True,
    trusted_hash: str=None,
    force: bool=False,
    ):
    '''Issue a systemctl command to a remote casper-node instance. This is a
    building block for being able to simulate bringing up/down a casper-node in
    a long-running network.

    This assumes that the given user's keys are installed on both this stests
    control machine as well as on the remote machine to connect to. The given
    user will also need to have sudo access on the remote machine.

    :param node: The `Node` to run the command on.
    :param ssh_user: The username to SSH into the remote machine as.
    :param command: The `systemctl` command to run on the casper-node service.
    :param ssh_key_path: The file path for the SSH key to use (default: `None`).
    :param check_rc: If `True`, raise an exception if the subprocess returns a
        non-zero exit code (default: `False`).
    :param trusted_hash: A trusted hash to use/inject when bringing a node up.
    :param force: If `True`, try and execute the systemctl command regardless
        of the current state of the node (default: `False`).

    :returns None
    '''

    utils.log(f'Current status for node #{node.index} is: {node.status}')

    # Check if it makes sense to execute this action, (e.g. "START" only if the
    # node is stopped).
    if not force:
        bail = False
        if command is SvcCommand.START and not node.status is NodeStatus.DOWN:
            bail = True
        elif command is SvcCommand.STOP and not node.status is NodeStatus.HEALTHY:
            bail = True

        if bail:
            utils.log(f"Skipping {command} command, node already is in matching status")
            return

    # Need to inject trusted hash.
    if command is SvcCommand.START and trusted_hash is not None:
        raise NotImplementedError("TODO: Add trusted hash injection")

    def yield_args():
        identity = f'{ssh_user}@{node.host}'

        utils.log(f'Making SSH connection as identity: {identity}')

        yield 'ssh'
        yield identity

        if ssh_key_path:
            utils.log(f'Using SSH key file: {ssh_key_path}')
            yield '-i'
            yield ssh_key_path

        remote_cli_cmd = f'sudo systemctl {command} casper-node-launcher.service'
        utils.log(f"Remote systemctl command: `{remote_cli_cmd}`")

        yield remote_cli_cmd

    subprocess.run(yield_args(), check=check_rc)

    # Update node status in cache.
    new_node_status = None
    if command is SvcCommand.STOP:
        new_node_status = NodeStatus.DOWN
    elif command is SvcCommand.START:
        new_node_status = NodeStatus.HEALTHY

    if new_node_status is not None:
        utils.log(f"Updating status = `{new_node_status}` for node #{node.index} in cache")
        node.status = new_node_status
        infra.set_node(node)

def common_main(svc_command: SvcCommand):
    """Common entry point for all svc-related node commands.

    Note: this function assumes that no CLI arg parsing has been done yet.

    :param svc_command: The service command to run on the remote casper node.

    """
    parser = get_arg_parser(svc_command)
    args = parser.parse_args()

    _, node = get_network_node(args)

    remote_node_systemctl(
        node=node,
        ssh_user=args.ssh_user,
        command=svc_command,
        ssh_key_path=args.ssh_key_path,
        check_rc=False,
        force=args.force,
    )
