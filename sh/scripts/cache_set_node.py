import argparse

from stests.core import cache
from stests.core import factory
from stests.core.types.infra import NodeGroup
from stests.core.types.infra import NodeType
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Upload node information to stests.")

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
    dest="node",
    help="Node index, e.g. 1.",
    type=args_validator.validate_node_index
    )

# Set CLI argument: node hostname.
ARGS.add_argument(
    "--hostname",
    default="localhost",
    dest="hostname",
    help="Node public hostname: {host}.",
    type=args_validator.validate_host
    )

# Set CLI argument: node RPC port.
ARGS.add_argument(
    "--rest-port",
    dest="port_rest",
    help="Node REST port: {port}.",
    type=args_validator.validate_port
    )

# Set CLI argument: node RPC port.
ARGS.add_argument(
    "--rpc-port",
    dest="port_rpc",
    help="Node RPC port: {port}.",
    type=args_validator.validate_port
    )

# Set CLI argument: node event stream port.
ARGS.add_argument(
    "--event-port",
    dest="port_event",
    help="Node event stream port: {port}.",
    type=args_validator.validate_port
    )

# Set CLI argument: node type.
ARGS.add_argument(
    "--type",
    choices=[i.name.lower() for i in NodeType],
    dest="typeof",
    help="Node type.",
    type=str
    )


def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    # Unpack.
    host = args.hostname
    index = int(args.node)
    network = args.network
    port_rest = int(args.port_rest)
    port_rpc = int(args.port_rpc)
    port_event = int(args.port_event)
    typeof = NodeType[args.typeof.upper()]

    # Instantiate.
    node = factory.create_node(
        group=NodeGroup.UNKNOWN,
        host=host,
        index=index,
        network_id=factory.create_network_id(network),
        port_rest=port_rest,
        port_rpc=port_rpc,
        port_event=port_event,
        typeof=typeof
    )

    # Push.
    cache.infra.set_node(node)

    # Notify.
    utils.log(f"Node {args.network}:{args.node} was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
