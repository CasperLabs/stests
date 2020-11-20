import argparse
import json

from stests import chain
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


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network, node = get_network_node(args)
    auction_info = chain.get_auction_info(network, node)

    if auction_info:
        print(json.dumps(auction_info, indent=4))
    else:
        print("Chain query returned null - is the auction contract correctly installed ?")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
