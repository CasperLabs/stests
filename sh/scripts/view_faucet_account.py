import argparse
import json
import typing

from stests import chain
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from arg_utils import get_network_node



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays a network's faucet balance.")

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
    default=1,
    dest="node",
    help="Node index, e.g. 1.",
    type=args_validator.validate_node_index
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network, node = get_network_node(args)
    account = chain.get_account(network, node, network.faucet.account_key)

    if account:
        print(json.dumps(account, indent=4))
    else:
        print("Chain query returned null - is the faucet correct ?")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
