import argparse

from stests.core import cache
from stests.core.domain import AccountStatus
from stests.core.domain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import crypto
from stests.core.utils import factory
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Register a network's system contracts with stests.")

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
    # Pull.
    network = cache.infra.get_network_by_name(args.network)
    if network is None:
        raise ValueError("Unregistered network.")

    print("TODO: register system contracts")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
