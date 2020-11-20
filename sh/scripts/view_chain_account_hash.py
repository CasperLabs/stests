import argparse

from stests.core import crypto
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays derived chain account identifier.")

# CLI argument: network name.
ARGS.add_argument(
    "--account",
    dest="account_key",
    help="An on-chain account identifier.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    account_hash = crypto.get_account_hash(args.account_key)

    utils.log(f"ACCOUNT HASH = {account_hash or 'N/A'}")


if __name__ == '__main__':
    main(ARGS.parse_args())
