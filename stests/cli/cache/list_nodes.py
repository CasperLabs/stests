import argparse

from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("List set of nodes registered with a network.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network_id=factory.create_network_id(args.network)
    network = cache.get_network(network_id)
    if network is None:
        logger.log_warning(f"Network {args.network} is unregistered.")
        return

    nodeset = cache.get_nodes(network_id)
    if not nodeset:
        logger.log_warning(f"Network {args.network} has no nodes.")
        return

    for node in sorted(nodeset, key=lambda i: i.index):
        logger.log(f"""NODE: {node.network}:N-{str(node.index).zfill(4)} -> {node.host}:{node.port} -> status={node.status.name}, type={node.typeof.name}""")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
