import argparse
import json

from stests import chain
from stests.core.utils import args_validator
from stests.core.utils import env
from arg_utils import get_network_node



# CLI argument parser.
ARGS = argparse.ArgumentParser("Renders on-chain block information.")

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

# CLI argument: block identifier.
ARGS.add_argument(
    "--block",
    dest="block_id",
    help="Block identifier.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    try:
        block_id = int(args.block_id)
    except:
        block_id = args.block_id

    _, node = get_network_node(args)
    block = node.get_block(block_id)

    if block:
        print(json.dumps(block, indent=4))
    else:
        print("Chain query returned null - is the block hash correct ?")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
