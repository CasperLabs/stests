import argparse

from stests.core.utils import factory
from stests.core.utils import logger
from stests.core.utils.args_factory import get_argparser_for_generator
from stests.generators.wg_110 import constants
from stests.generators.wg_110.args import Arguments
from stests.orchestration.predicates import is_run_locked



# Set command line arguments.
ARGS = get_argparser_for_generator(f"Executes {constants.DESCRIPTION} workflow.")

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

# CLI argument: user accounts.
ARGS.add_argument(
    "--user-accounts",
    help=f"Number of user accounts to generate. Default={constants.USER_ACCOUNTS}",
    dest="user_accounts",
    type=int,
    default=constants.USER_ACCOUNTS
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

    # Unpack args.
    network_id = factory.create_network_id(args.network_name)
    node_id = factory.create_node_id(network_id, args.node_index)

    # Set execution context.
    ctx = factory.create_run_info(
        args=Arguments.create(args),
        loop_count=args.loop_count,
        loop_interval=args.loop_interval,
        network_id=network_id,
        node_id=node_id,
        run_index=args.run_index,
        run_type=constants.TYPE
    )

    # Abort if a run lock cannot be acquired.
    if is_run_locked(ctx):
        logger.log_warning(f"{constants.TYPE} :: run {args.run_index} aborted as it is currently executing.")
        
    # Start run.
    else:
        from stests.orchestration.actors import do_run
        do_run.send(ctx)
        logger.log(f"{constants.TYPE} :: run {args.run_index} started")


# Invoke entry point.
main(ARGS.parse_args())
