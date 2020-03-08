import argparse

from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger

from stests.generators.wg_100 import constants
from stests.generators.wg_100.args import Arguments



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes {constants.DESCRIPTION} workflow.")

# CLI argument: network name.
ARGS.add_argument(
    "network_name",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: scope -> node index.
ARGS.add_argument(
    "--node",
    dest="node_index",
    help="Node index - must be between 1 and 999. If specified deploys are dispatched to this node only, otherwise deploys are dispatched to random nodes.",
    type=args_validator.validate_node_index,
    default=0,
    required=False
    )

# CLI argument: scope -> run index.
ARGS.add_argument(
    "--run",
    dest="run_index",
    help="Generator run index - must be between 1 and 65536.",
    type=args_validator.validate_run_index,
    default=1
    )

# CLI argument: scope -> run index.
ARGS.add_argument(
    "--loop-interval",
    dest="loop_interval",
    help="Interval in seconds between loops.",
    type=args_validator.validate_loop_interval,
    default=0
    )

# CLI argument: scope -> run index.
ARGS.add_argument(
    "--loop-count",
    dest="loop_count",
    help="Number of times to loop.",
    type=args_validator.validate_loop_count,
    default=0
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
    # Import initialiser to setup upstream services / actors.
    import stests.initialiser

    # Set run context.
    network_id = factory.create_network_id(args.network_name)
    node_id = factory.create_node_id(network_id, args.node_index)
    ctx = factory.create_run_context(
        args=Arguments.create(args),
        loop_count=args.loop_count,
        loop_interval=args.loop_interval,
        network_id=network_id,
        node_id=node_id,
        run_index=args.run_index,
        run_type=constants.TYPE
    )

    # Start workflow.
    from stests.orchestration.actors import do_run
    do_run.send(ctx)
    logger.log("WG-100 :: generator executed")


# Invoke entry point.
main(ARGS.parse_args())
