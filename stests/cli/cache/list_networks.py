import argparse

from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("Lists set of registered networks.")


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    for network in cache.get_networks():
        print(network)
        logger.log(f"""NETWORK: {network.name} -> status={network.status.name}, type={network.typeof.name}, index={network.index}""")

# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
