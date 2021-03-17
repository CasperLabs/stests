import argparse
import enum
import subprocess
import typing as tp
from pathlib import Path

from stests.core.cache.ops import infra
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from stests.core.types.infra import Node
from stests.core.types.infra.enums import NodeStatus
from sh.scripts.arg_utils import get_network_node

class SvcCommand(str, enum.Enum):
    STOP = 'stop'
    START = 'start'

def get_healthy_and_down_nodes(network) -> tp.Tuple[tp.List[Node], tp.List[Node]]:
    utils.log(f'Fetching all nodes')
    nodes = infra.get_nodes(network)
    num_total_nodes = len(nodes)
    utils.log(f'Found {num_total_nodes} node(s) in total')

    utils.log('Filtering out healthy nodes')
    healthy_nodes = [n for n in nodes if n.status is NodeStatus.HEALTHY]
    utils.log(f'Found {len(healthy_nodes)} healthy node(s)')

    utils.log('Filtering out down nodes')
    down_nodes = [n for n in nodes if n.status is NodeStatus.DOWN]
    utils.log(f'Found {len(down_nodes)} down node(s)')

    return healthy_nodes, down_nodes

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

def remote_node_ssh_invoke(
    ssh_user: str,
    ssh_host: str,
    to_run: str,
    ssh_key_path: str=None,
):
    def yield_args():
        identity = f'{ssh_user}@{ssh_host}'

        utils.log(f'Making SSH connection as identity: {identity}')

        yield 'ssh'
        yield identity

        if ssh_key_path:
            utils.log(f'Using SSH key file: {ssh_key_path}')
            yield '-i'
            yield ssh_key_path

        utils.log(f"Remote systemctl command: `{to_run}`")

        yield to_run

    subprocess.run(yield_args(), check=True)

def remote_node_ssh_rsync(
    source_path: Path,
    ssh_user: str,
    ssh_host: str,
    target_dir: Path,
    ssh_key_path: str=None,
    use_remote_sudo: bool=True,
):
    utils.log(f'Copying `{source_path}` to {ssh_host}:{target_dir} using `rsync`')

    def yield_args():
        identity = f'{ssh_user}@{ssh_host}'

        utils.log(f'Making connection as identity: {identity}')

        yield 'rsync'
        yield '-avz'
        yield '-q'

        if use_remote_sudo:
            utils.log('Using `sudo` on remote target')
            yield '--rsync-path="sudo rsync"'

        if ssh_key_path:
            utils.log(f'Using SSH key file: {ssh_key_path}')

            # With `rsync`, this needs to be passed in as a suboption to `ssh`.
            yield '-e'
            yield f'ssh -i {ssh_key_path}'

        yield source_path

        target = f'{identity}:{target_dir}'

        yield target

    subprocess.run(yield_args(), check=True)

def remote_node_ssh_copy(
    source_path: Path,
    ssh_user: str,
    ssh_host: str,
    target_dir: Path,
    ssh_key_path: str=None,
):
    utils.log(f'Copying `{source_path}` to {ssh_host}:{target_dir}')

    def yield_args():
        identity = f'{ssh_user}@{ssh_host}'

        utils.log(f'Making SSH connection as identity: {identity}')

        yield 'scp'
        yield '-r'
        # yield '-q'

        if ssh_key_path:
            utils.log(f'Using SSH key file: {ssh_key_path}')
            yield '-i'
            yield ssh_key_path

        yield source_path

        target = f'{identity}:{target_dir}'

        yield target

    subprocess.run(yield_args(), check=True)

def remote_node_systemctl(
    node: Node,
    ssh_user: str,
    command: SvcCommand,
    ssh_key_path: Path=None,
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

    # TODO: This might not need to be done anymore, casper-launcher seems to
    #       take care of this?
    # # Need to inject trusted hash.
    # if command is SvcCommand.START and trusted_hash is not None:
    #     raise NotImplementedError("TODO: Add trusted hash injection")

    remote_node_ssh_invoke(
        ssh_user=ssh_user,
        ssh_host=node.host,
        to_run=f'sudo systemctl {command} casper-node-launcher.service',
        ssh_key_path=ssh_key_path,
    )

    # def yield_args():
    #     identity = f'{ssh_user}@{node.host}'

    #     utils.log(f'Making SSH connection as identity: {identity}')

    #     yield 'ssh'
    #     yield identity

    #     if ssh_key_path:
    #         utils.log(f'Using SSH key file: {ssh_key_path}')
    #         yield '-i'
    #         yield ssh_key_path

    #     remote_cli_cmd = f'sudo systemctl {command} casper-node-launcher.service'
    #     utils.log(f"Remote systemctl command: `{remote_cli_cmd}`")

    #     yield remote_cli_cmd

    # subprocess.run(yield_args(), check=True)

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
        force=args.force,
    )
