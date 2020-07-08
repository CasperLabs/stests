import argparse

from stests.core import cache
from stests.core import factory
from stests.core.types.infra import NodeStatus
from stests.core.utils import args_validator
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Informs stests of a mutation in the status of a node.")

# CLI argument: node reference.
ARGS.add_argument(
    "node",
    help="Node name: {network-type}{network-index}:{node-index}.",
    type=args_validator.validate_node_name
    )

# Set CLI argument: node status.
ARGS.add_argument(
    "status",
    choices=[i.name.lower() for i in NodeStatus],
    help="Node status.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    network_id = factory.create_network_id(args.node.split(':')[0])
    node_id = factory.create_node_id(network_id, int(args.node.split(':')[-1]))

    # Pull.
    node = cache.infra.get_node_by_identifier(node_id)
    if node is None:
        raise ValueError("Unregistered node.")

    # Update.
    node.status = NodeStatus[args.status.upper()]

    # Push.
    cache.infra.set_node(node)

    # Notify.
    utils.log(f"Node {args.node} status was updated --> {node.status}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
