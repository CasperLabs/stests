import argparse
import subprocess
from pathlib import Path

from stests import chain
from stests.core import crypto
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from stests.core.types.infra import Node
from .arg_utils import get_network_node
from .svc_utils import get_arg_parser
from .svc_utils import remote_node_systemctl
from .svc_utils import SvcCommand

SVC_COMMAND = SvcCommand.STOP

def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    utils.log(f"Executing `systemctl {args.command}`:")

    _, node = get_network_node(args)

    remote_node_systemctl(
        node=node,
        ssh_user=args.ssh_user,
        command=SVC_COMMAND,
        ssh_key_path=args.ssh_key_path,
        check_rc=False,
    )

# TODO: Just for testing, remove.
if __name__ == '__main__':
    parser = get_arg_parser(SVC_COMMAND)
    main(parser.parse_args())
