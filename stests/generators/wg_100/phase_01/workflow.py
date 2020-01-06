import argparse

from stests.core.mq import dramatiq
from stests.core.mq import init as init_mq_broker
from stests.core.types.core import ExecutionContext
from stests.generators.wg_100 import metadata
from stests.utils import env

# Default number of user accounts to generate.
DEFAULT_USER_ACCOUNTS = 5

# Default number of bids to submit per user account.
DEFAULT_BIDS_PER_ACCOUNT = 1

# Default filename of the contract's wasm blob.
DEFAULT_CONTRACT_WASM_FILENAME = "erc20_smart_contract"

# Default name of ERC20 token for which an auction is being simulated.
DEFAULT_TOKEN_NAME = "ABC"

# Default supply of ERC20 token = 20k.
DEFAULT_TOKEN_SUPPLY = int(2e4)

# Default user's CLX balance = 1m.
DEFAULT_USER_CLX_BALANCE = int(1e7)

# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes the {metadata.DESCRIPTION} workload generator.")
# ... execution context arguments
# TODO: specify
ARGS.add_argument(
    "--simulator-run-id",
    help="Simulator run identifier.",
    dest="simulator_run_id",
    type=int,
    default=0
    )

ARGS.add_argument(
    "--network-id",
    help="Network identifier.",
    dest="network_id",
    type=str,
    default=env.get_network_id()
    )

# ... generator specific arguments
ARGS.add_argument(
    "--bids-per-account",
    help="Number of bids per account to submit.",
    dest="bids_per_accounts",
    type=int,
    default=DEFAULT_BIDS_PER_ACCOUNT
    )

ARGS.add_argument(
    "--contract-name",
    help="Name of smart contract to be loaded from resources directory.",
    dest="contract_name",
    type=str,
    default=DEFAULT_CONTRACT_WASM_FILENAME
    )

# TODO: specify
ARGS.add_argument(
    "--faucet-account",
    help="Address of a faucet smart contract.",
    dest="faucet_account",
    type=str
    )

ARGS.add_argument(
    "--user-initial-clx-balance",
    help="Initial CLX balance of user accounts.",
    dest="user_initial_clx_balance",
    type=int,
    default=DEFAULT_USER_CLX_BALANCE
    )

ARGS.add_argument(
    "--max-user-accounts",
    help="Maximum number of user accounts to generate.",
    dest="max_user_accounts",
    type=int,
    default=DEFAULT_USER_ACCOUNTS
    )

ARGS.add_argument(
    "--token-name",
    help="Name of ERC20 token for which an auction is being simulated.",
    dest="token_name",
    type=str,
    default=DEFAULT_TOKEN_NAME
    )

ARGS.add_argument(
    "--token-supply",
    help="Total amount of ERC20 token to be issued.",
    dest="token_supply",
    type=int,
    default=DEFAULT_TOKEN_SUPPLY
    )

def get_pipeline_for_contract(actors, ctx):
    """Returns a pipeline to initialise a contract account.
    
    """
    return \
        actors.contract.create_account.message(ctx, 0) | \
        actors.contract.cache_account.message()


def get_pipeline_for_user(actors, ctx, index):
    """Returns a pipeline to initialise a user account.
    
    """
    return \
        actors.user.create_account.message(ctx, index) | \
        actors.user.cache_account.message()


def get_group_for_users(actors, ctx, max_user_accounts):
    """Returns a group to initialise a set of user accounts.
    
    """
    return dramatiq.group(map(
        lambda index: get_pipeline_for_user(actors, ctx, index), 
        range(max_user_accounts)
    ))


def get_workflow(actors, ctx, max_user_accounts):
    """Returns a workflow that initialises accounts, resources ...etc, 
       in readiness for system test execution.
    
    """
    return dramatiq.group([
        get_pipeline_for_contract(actors, ctx),
        get_group_for_users(actors, ctx, max_user_accounts)
        ])


def main():
    """Workflow entry point.
    
    """
    # Initialise execution context.
    ctx = ExecutionContext(ARGS.network_id, metadata.ID, ARGS.simulator_run_id)

    # Initialise mq broker.
    init_mq_broker(ctx.network_id)

    # Import actors.
    # Note: currently we must import actors AFTER the mq broker is initiialised.
    from stests.generators.wg_100.phase_01 import actors

    # Execute workflow.
    workflow = get_workflow(actors, ctx, ARGS.max_user_accounts)
    workflow.run()



if __name__ == "__main__":
    ARGS = ARGS.parse_args()
    main()