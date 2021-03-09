import subprocess
from pathlib import Path

from stests.core.types.infra import Node

def remote_node_systemctl(
    node: Node,
    ssh_user: str,
    command: str,
    ssh_key_path: Path=None,
    check_rc: bool=False,
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

    def yield_args():
        yield 'ssh'
        yield f'{ssh_user}@{node.host}'

        if ssh_key_path:
            yield '-i'
            yield ssh_key_path

        yield f'sudo systemctl {command} casper-node.service'

    subprocess.run(yield_args(), check=check_rc)
