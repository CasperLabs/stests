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

    return parser

def remote_node_systemctl(
    node: Node,
    ssh_user: str,
    command: SvcCommand,
    ssh_key_path: Path=None,
    check_rc: bool=True,
    trusted_hash: str=None,
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

    :returns None
    '''

    utils.log(f'Current status for node #{node.index} is: {node.status}')

    # Check if it makes sense to execute this action, (e.g. "START" only if the
    # node is stopped).
    if command is SvcCommand.START and not node.status is NodeStatus.DOWN:
        return
    elif command is SvcCommand.STOP and not node.status is NodeStatus.HEALTHY:
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

        yield f'sudo systemctl {command} casper-node-launcher.service'

    subprocess.run(yield_args(), check=check_rc)

    # Update node status in cache.
    if command is SvcCommand.STOP:
        node.status = NodeStatus.DOWN
    elif command is SvcCommand.START:
        node.status = NodeStatus.HEALTHY

    infra.set_node(node)
