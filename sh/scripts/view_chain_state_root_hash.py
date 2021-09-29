import argparse

from stests import chain
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from arg_utils import get_network_node
from arg_utils import get_network_nodeset



# CLI argument parser.
ARGS = argparse.ArgumentParser("Renders a state root hash as reported by node.")

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
        
    if args.node:
        _, node = get_network_node(args)
        nodeset = [node]
    else:
        _, nodeset = get_network_nodeset(args)
    
    for node in nodeset:
        try:
            state_root_hash = node.get_state_root_hash(block_id)
        except:
            utils.log(f"STATE ROOT HASH @ {node.address_rpc} = 'N/A'")
        else:
            utils.log(f"STATE ROOT HASH @ {node.address_rpc} = {state_root_hash or 'N/A'}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
