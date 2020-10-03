import argparse
import json
import typing

from stests.core import clx
from stests.core import factory
from stests.core.utils import args_validator



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays deploy information returned by a chain query.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default="nctl1",
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: run type.
ARGS.add_argument(
    "--deploy-hash",
    "deploy_hash",
    dest="",
    help="Deploy hash.",
    type=str,
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    _render(clx.get_deploy_info(
        factory.create_network_id(args.network),
        args.deploy_hash
        ))


def _render(info: typing.Dict[str, typing.Union[str, int]]):
    """Renders on-chain deploy information.
    
    """
    print("--------------------------------------------------------------------------------------------")
    if info:
        print(json.dumps(info, indent=4))
    else:
        print("Chain query returned null - is the deploy hash correct ?")
    print("--------------------------------------------------------------------------------------------")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
