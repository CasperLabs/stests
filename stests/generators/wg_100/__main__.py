import argparse
from dataclasses import dataclass
from dataclasses_json import dataclass_json

import dramatiq 

from stests.core import mq
from stests.core.utils import args_validator
from stests.core.utils import logger
from stests.generators.wg_100 import constants
from stests.generators.wg_100.actors import orchestrator
from stests.generators.wg_100.ctx import Arguments
from stests.generators.wg_100.ctx import Context



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes {constants.DESCRIPTION} workflow.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network_name
    )

# CLI argument: scope -> node index.
ARGS.add_argument(
    "--node",
    dest="node",
    help="Node index - must be between 1 and 999. If specified deploys are dispatched to this node only, otherwise deploys are dispatched to random nodes.",
    type=args_validator.validate_node_index,
    default=1,
    required=False
    )

# CLI argument: scope -> run index.
ARGS.add_argument(
    "--run",
    dest="run",
    help="Generator run index - must be between 1 and 65536.",
    type=args_validator.validate_generator_run_idx,
    default=1
    )

# CLI argument: token name.
ARGS.add_argument(
    "--token-name",
    help=f"Name of ERC-20 token.  Default={constants.TOKEN_NAME}",
    dest="token_name",
    type=str,
    default=constants.TOKEN_NAME
    )

# CLI argument: token supply.
ARGS.add_argument(
    "--token-supply",
    help=f"Amount of ERC-20 token to be issued. Default={constants.TOKEN_SUPPLY}",
    dest="token_supply",
    type=int,
    default=constants.TOKEN_SUPPLY
    )

# CLI argument: user accounts.
ARGS.add_argument(
    "--user-accounts",
    help=f"Number of user accounts to generate. Default={constants.USER_ACCOUNTS}",
    dest="user_accounts",
    type=int,
    default=constants.USER_ACCOUNTS
    )

# CLI argument: bids / user.
ARGS.add_argument(
    "--user-bids",
    help=f"Number of bids per user to submit. Default={constants.USER_BIDS}",
    dest="user_bids",
    type=int,
    default=constants.USER_BIDS
    )

# CLI argument: initial CLX balance.
ARGS.add_argument(
    "--user-initial-clx-balance",
    help=f"Initial CLX balance of user accounts. Default={constants.USER_INITIAL_CLX_BALANCE}",
    dest="user_initial_clx_balance",
    type=int,
    default=constants.USER_INITIAL_CLX_BALANCE
    )


def execute(args: argparse.Namespace):
    """Entry point.
    
    """
    logger.log("... instantiating execution context")
    ctx: Context = Context.create(
        args=Arguments.create(args),
        network=args.network,
        node=args.node,
        run=args.run,
        typeof=constants.TYPE    
        )

    logger.log("... invoking orchestrator")
    orchestrator.execute(ctx)


# Invoke entry point.
execute(ARGS.parse_args())
