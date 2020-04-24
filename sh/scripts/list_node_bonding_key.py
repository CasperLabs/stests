import argparse

from stests.core import cache
from stests.core.types.chain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import crypto
from stests.core import factory
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Lists a node's bonding asymmetric key pair.")

# CLI argument: node reference.
ARGS.add_argument(
    "node",
    help="Node name: {network-type}{network-index}:{node-index}.",
    type=args_validator.validate_node_name
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    network_id = factory.create_network_id(args.node.split(':')[0])
    node_id = factory.create_node_id(network_id, int(args.node.split(':')[-1]))

    # Pull.
    node = cache.infra.get_node(node_id)
    if node is None:
        logger.log_warning("Unregistered node.")
        return
    if node.account is None:
        logger.log_warning("Unregistered node bonding key.")
        return

    # Inform.
    logger.log(f"""NODE: {node.label} -> bonding pvk {node.account.private_key}""")
    logger.log(f"""NODE: {node.label} -> bonding pbk {node.account.public_key}""")

# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
