import argparse
import json

from stests import chain
from stests.core import crypto
from stests.core.utils import args_validator
from stests.core.utils import env
from arg_utils import get_network_node



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays on-chain account information.")

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

# CLI argument: account identifer.
ARGS.add_argument(
    "--account",
    dest="account_key",
    help="A 33 byte account key: a public key prefixed by a single byte to inidcate key type.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network, node = get_network_node(args)
    account = chain.get_account(network, node, args.account_key)

    if account:
        print(json.dumps(account, indent=4))
    else:
        print("Chain query returned null - is the account key correct ?")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
