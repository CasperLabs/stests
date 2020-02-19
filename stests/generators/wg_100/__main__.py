import argparse
from dataclasses import dataclass
from dataclasses_json import dataclass_json

import dramatiq 

from stests.core import mq
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger
from stests.generators.wg_100 import constants
from stests.generators.wg_100.args import Arguments



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes {constants.DESCRIPTION} workflow.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
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
    type=args_validator.validate_run_index,
    default=1
    )

# CLI argument: initial CLX balance.
ARGS.add_argument(
    "--faucet-initial-clx-balance",
    help=f"Initial CLX balance of faucet account. Default={constants.FAUCET_INITIAL_CLX_BALANCE}",
    dest="faucet_initial_clx_balance",
    type=int,
    default=constants.FAUCET_INITIAL_CLX_BALANCE
    )


# CLI argument: initial CLX balance.
ARGS.add_argument(
    "--contract-initial-clx-balance",
    help=f"Initial CLX balance of contract account. Default={constants.CONTRACT_INITIAL_CLX_BALANCE}",
    dest="contract_initial_clx_balance",
    type=int,
    default=constants.CONTRACT_INITIAL_CLX_BALANCE
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


def main(args: argparse.Namespace):
    """Entry point.
    
    """
    # Initialise MQ sub-package & import actors in scope.
    mq.initialise()


    # Import actors in scope.
    import stests.core.actors
    import stests.generators.wg_100.orchestration
    import stests.generators.wg_100.phase_1

    # Set run context.
    network_id = factory.create_network_id(args.network)
    node_id = factory.create_node_id(network_id, args.node)
    ctx = factory.create_run_context(
        args=Arguments.create(args),
        network_id=network_id,
        node_id=node_id,
        run_index=args.run,
        run_type=constants.TYPE
    )

    # Send spinup message.
    logger.log("... spinup begins")
    from stests.core.actors.misc import do_flush_cache
    from stests.generators.wg_100.orchestration import on_flush_cache
    do_flush_cache.send_with_options(
        args=(ctx, ), 
        on_success=on_flush_cache
        )


# Invoke entry point.
main(ARGS.parse_args())
