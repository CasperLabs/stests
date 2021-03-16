from sh.scripts.arg_utils import get_network_node
from sh.scripts.svc_utils import get_arg_parser
from sh.scripts.svc_utils import get_healthy_nodes
from sh.scripts.svc_utils import remote_node_systemctl
from sh.scripts.svc_utils import SvcCommand

SVC_COMMAND = SvcCommand.STOP

def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    network, node = get_network_node(args)

    get_healthy_nodes(network)

if __name__ == '__main__':
    parser = get_arg_parser(SVC_COMMAND)
    main(parser.parse_args())
