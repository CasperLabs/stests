import argparse

from stests import chain
from stests.core import crypto
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from utils import get_network_node



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays an on-chain account balance.")

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
    help="Either a 33 byte account id (hex format) or a 32 byte account hash (hex format).",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network, node = get_network_node(args)
    account_hash = args.account_key if len(args.account_key) == 64 else \
                   crypto.get_account_hash(args.account_key)
    account = chain.get_account(network, node, account_hash)
    purse_uref = account['Account']['main_purse']
    balance = chain.get_account_balance(network, node, purse_uref)
    utils.log(f"ACCOUNT BALANCE = {balance or 'N/A'}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
