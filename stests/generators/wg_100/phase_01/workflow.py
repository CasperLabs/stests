import argparse

from stests.core import mq
from stests.core.types import NetworkType
from stests.core.utils import args_validator
from stests.core.utils import encoder
from stests.core.utils import env
from stests.core.utils.generator import GeneratorContext
from stests.core.utils.generator import GeneratorScope
from stests.generators.wg_100 import defaults
from stests.generators.wg_100 import metadata
from stests.generators.wg_100.phase_01.args import Arguments
from stests.generators.wg_100.phase_01.factory import get_workflow



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes {metadata.DESCRIPTION} workflow.")

# CLI argument: network type.
ARGS.add_argument(
    "--network-type",
    dest="network_type",
    choices=[i.name.lower() for i in NetworkType],
    help="Type of network being tested.",
    type=str
    )

# CLI argument: network index.
ARGS.add_argument(
    "--network-idx",
    dest="network_idx",
    help="Network index - must be between 1 and 99.",
    type=args_validator.validate_network_idx,
    default=1
    )

# CLI argument: node index.
ARGS.add_argument(
    "--node-idx",
    dest="node_idx",
    help="Node index - must be between 1 and 999. If specified deploys are dispatched to this node only, otherwise deploys are dispatched to random nodes.",
    type=args_validator.validate_node_idx,
    default=1,
    required=False
    )

# Workflow identifer.
ARGS.add_argument(
    "--generator-idx",
    dest="generator_run_idx",
    help="Generator run index - must be between 1 and 65536.",
    type=args_validator.validate_generator_run_idx,
    default=1
    )

ARGS.add_argument(
    "--token-name",
    help=f"Name of ERC-20 token.  Default={defaults.TOKEN_NAME}",
    dest="token_name",
    type=str,
    default=defaults.TOKEN_NAME
    )

ARGS.add_argument(
    "--token-supply",
    help=f"Amount of ERC-20 token to be issued. Default={defaults.TOKEN_SUPPLY}",
    dest="token_supply",
    type=int,
    default=defaults.TOKEN_SUPPLY
    )

ARGS.add_argument(
    "--user-accounts",
    help=f"Number of user accounts to generate. Default={defaults.USER_ACCOUNTS}",
    dest="user_accounts",
    type=int,
    default=defaults.USER_ACCOUNTS
    )

ARGS.add_argument(
    "--user-bids",
    help=f"Number of bids per user to submit. Default={defaults.USER_BIDS}",
    dest="user_bids",
    type=int,
    default=defaults.USER_BIDS
    )

ARGS.add_argument(
    "--user-initial-clx-balance",
    help=f"Initial CLX balance of user accounts. Default={defaults.USER_INITIAL_CLX_BALANCE}",
    dest="user_initial_clx_balance",
    type=int,
    default=defaults.USER_INITIAL_CLX_BALANCE
    )


def main():
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Set cli arguments.
    args = ARGS.parse_args()

    # Set scope.
    scope = GeneratorScope(args)

    # Set context.

    ctx = GeneratorContext(Arguments, metadata, args)

    print(ctx.scope.to_dict())

    # Set arguments.
    # args = Arguments.create(ARGS.parse_args())

    # Framework requirement: register arguments type.
    # encoder.register_type(Arguments)

    # # Framework requirement: initialise broker.
    # mq.init_broker(args.network_id)

    # # Execute workflow.
    # workflow = get_workflow(args)
    # workflow.run()


# Entry point.
if __name__ == '__main__':
    main()