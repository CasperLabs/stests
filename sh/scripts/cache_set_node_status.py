import argparse

from stests.core import cache
from stests.core import factory
from stests.core.types.infra import NodeStatus
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env


# CLI argument parser.
ARGS = argparse.ArgumentParser("Updates node status within stests cache.")

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

# Set CLI argument: node status.
ARGS.add_argument(
    "--status",
    choices=[i.name.lower() for i in NodeStatus],
    dest="status",
    help="Node status.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    network_id = factory.create_network_id(args.network)
    node_id = factory.create_node_id(network_id, int(args.node))

    # Pull.
    node = cache.infra.get_node(node_id)
    if node is None:
        raise ValueError("Unregistered node.")

    # Update.
    node.status = NodeStatus[args.status.upper()]

    # Push.
    cache.infra.set_node(node)

    # Notify.
    utils.log(f"Node {args.network}:{args.node} status was updated --> {node.status}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
