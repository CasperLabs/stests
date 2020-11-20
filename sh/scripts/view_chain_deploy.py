import argparse
import json

from stests import chain
from stests.core.utils import args_validator
from stests.core.utils import env
from arg_utils import get_network_node


# CLI argument parser.
ARGS = argparse.ArgumentParser("Renders on-chain deploy information.")

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

# CLI argument: deploy hash.
ARGS.add_argument(
    "--deploy",
    dest="deploy_hash",
    help="Deploy hash.",
    type=str,
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network, node = get_network_node(args)
    deploy = chain.get_deploy(network, node, args.deploy_hash)
    if deploy:
        print(json.dumps(deploy, indent=4))
    else:
        print("Chain query returned null - is the deploy hash correct ?")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
