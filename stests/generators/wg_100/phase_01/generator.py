import argparse

import dramatiq 

from stests.core.types import NetworkType
from stests.core.utils import args_validator
from stests.generators.wg_100 import defaults
from stests.generators.wg_100 import metadata
from stests.generators.wg_100.phase_01.generator_ctx import Context



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes {metadata.DESCRIPTION} workflow.")

# CLI argument: scope -> network type.
ARGS.add_argument(
    "--network-type",
    dest="network_type",
    choices=[i.name.lower() for i in NetworkType],
    help="Type of network being tested.",
    type=str,
    default=NetworkType.LOC.name.lower()
    )

# CLI argument: scope -> network index.
ARGS.add_argument(
    "--network-idx",
    dest="network_idx",
    help="Network index - must be between 1 and 99.",
    type=args_validator.validate_network_idx,
    default=1
    )

# CLI argument: scope -> node index.
ARGS.add_argument(
    "--node-idx",
    dest="node_idx",
    help="Node index - must be between 1 and 999. If specified deploys are dispatched to this node only, otherwise deploys are dispatched to random nodes.",
    type=args_validator.validate_node_idx,
    default=1,
    required=False
    )

# CLI argument: scope -> run index.
ARGS.add_argument(
    "--run-idx",
    dest="run_idx",
    help="Generator run index - must be between 1 and 65536.",
    type=args_validator.validate_generator_run_idx,
    default=1
    )

# CLI argument: token name.
ARGS.add_argument(
    "--token-name",
    help=f"Name of ERC-20 token.  Default={defaults.TOKEN_NAME}",
    dest="token_name",
    type=str,
    default=defaults.TOKEN_NAME
    )

# CLI argument: token supply.
ARGS.add_argument(
    "--token-supply",
    help=f"Amount of ERC-20 token to be issued. Default={defaults.TOKEN_SUPPLY}",
    dest="token_supply",
    type=int,
    default=defaults.TOKEN_SUPPLY
    )

# CLI argument: user accounts.
ARGS.add_argument(
    "--user-accounts",
    help=f"Number of user accounts to generate. Default={defaults.USER_ACCOUNTS}",
    dest="user_accounts",
    type=int,
    default=defaults.USER_ACCOUNTS
    )

# CLI argument: bids / user.
ARGS.add_argument(
    "--user-bids",
    help=f"Number of bids per user to submit. Default={defaults.USER_BIDS}",
    dest="user_bids",
    type=int,
    default=defaults.USER_BIDS
    )

# CLI argument: initial CLX balance.
ARGS.add_argument(
    "--user-initial-clx-balance",
    help=f"Initial CLX balance of user accounts. Default={defaults.USER_INITIAL_CLX_BALANCE}",
    dest="user_initial_clx_balance",
    type=int,
    default=defaults.USER_INITIAL_CLX_BALANCE
    )


def get_workflow(ctx: Context):
    """Workflow instance factory.

    :param ctx: Contextual information passed along actor chain.

    """
    # NOTE: currently a framework requirement as we need to defer workflow
    #       instantiation until after MQ broker connection is established.
    from stests.generators.wg_100.phase_01.actors import get_workflow as _get_workflow

    return _get_workflow(ctx)


# Entry point.
if __name__ == '__main__':
    Context.execute(ARGS.parse_args(), get_workflow)
