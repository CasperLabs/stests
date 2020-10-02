import argparse

from stests.core import crypto
from stests.core.utils import cli as utils


# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays derived account identifier.")

# CLI argument: network name.
ARGS.add_argument(
    "public_key",
    help="Hexadecimal representation of a public key associated with an account.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    account_id = crypto.get_account_id(crypto.KeyAlgorithm.ED25519, args.public_key)
    utils.log(account_id)


if __name__ == '__main__':
    main(ARGS.parse_args())
