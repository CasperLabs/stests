import argparse

from stests import chain
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from arg_utils import get_network_node
from arg_utils import get_network_nodeset



# CLI argument parser.
ARGS = argparse.ArgumentParser("Renders height of chain at node(s).")

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
    dest="node",
    help="Node index, e.g. 1.",
    type=args_validator.validate_node_index
    )


def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    if args.node:
        network, node = get_network_node(args)
        nodeset = [node]
    else:
        network, nodeset = get_network_nodeset(args)
    
    for node in nodeset:
        block = chain.get_block(network, node)
        try:
            era_id = block['header']['era_id']
        except:
            era_id = "N/A"
        try:
            height = block['header']['height']
        except:
            height = "N/A"
        utils.log(f"ERA::HEIGHT @ {node.address_rpc} = {era_id}::{height}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
