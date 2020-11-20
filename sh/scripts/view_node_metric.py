import argparse
import json

from stests import chain
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from arg_utils import get_network_node
from arg_utils import get_network_nodeset


# CLI argument parser.
ARGS = argparse.ArgumentParser("Renders node metrics information.")

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

# CLI argument: metric of interest.
ARGS.add_argument(
    "--metric",
    default="*",
    dest="metric",
    help="Specific metric to view.",
    type=str
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
        utils.log_line()
        utils.log(f"NODE METRICS @ NODE {node.index} :: {node.address_rpc}:")
        for metric in chain.get_node_metrics(network, node).split("\n"):
            if args.metric == "*" or metric.startswith(args.metric):
                print(metric)

    utils.log_line()


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
