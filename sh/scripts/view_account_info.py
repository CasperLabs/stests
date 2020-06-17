import argparse
import json
import typing

from stests.core import clx
from stests.core import factory
from stests.core.utils import args_validator
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays an on-chain account information.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: network name.
ARGS.add_argument(
    "account",
    help="Network account (hex format), e.g. 853b4f5e2cb1e05416dc8af8ebdfae792b5c7b9246172450c0df9bff88c28297.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    _render(clx.get_account_info(
        factory.create_network_id(args.network),
        args.account
        ))


def _render(info: typing.Dict[str, typing.Union[str, int]]):
    """Renders on-chain deploy information.
    
    """
    print("--------------------------------------------------------------------------------------------")
    if info:
        print(json.dumps(info, indent=4))
    else:
        print("Chain query returned null - is the address correct ?")
    print("--------------------------------------------------------------------------------------------")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
