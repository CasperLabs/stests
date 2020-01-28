import argparse

from stests.core import mq
from stests.core.utils import encoder
from stests.core.utils import env
from stests.generators.wg_100 import defaults
from stests.generators.wg_100 import metadata
from stests.generators.wg_100.phase_01.args import Arguments
from stests.generators.wg_100.phase_01.factory import get_workflow



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes {metadata.DESCRIPTION} workflow.")

# Network identifer.
ARGS.add_argument(
    "--network-id",
    help="Identifier of network being tested.",
    dest="network_id",
    type=str,
    default=env.get_network_id()
    )

# Workflow identifer.
ARGS.add_argument(
    "--workflow-id",
    help="Identifier of workflow being executed.",
    dest="workflow_id",
    type=int,
    default=0
    )

ARGS.add_argument(
    "--token-name",
    help="Name of ERC-20 token.",
    dest="token_name",
    type=str,
    default=defaults.TOKEN_NAME
    )

ARGS.add_argument(
    "--token-supply",
    help="Amount of ERC-20 token to be issued.",
    dest="token_supply",
    type=int,
    default=defaults.TOKEN_SUPPLY
    )

ARGS.add_argument(
    "--user-accounts",
    help="Number of user accounts to generate.",
    dest="user_accounts",
    type=int,
    default=defaults.USER_ACCOUNTS
    )

ARGS.add_argument(
    "--user-bids",
    help="Number of bids per user to submit.",
    dest="user_bids",
    type=int,
    default=defaults.USER_BIDS
    )

ARGS.add_argument(
    "--user-initial-clx-balance",
    help="Initial CLX balance of user accounts.",
    dest="user_initial_clx_balance",
    type=int,
    default=defaults.USER_INITIAL_CLX_BALANCE
    )

ARGS.add_argument(
    "--wasm-contract-name",
    help="Name of smart contract .wasm file.",
    dest="wasm_contract_name",
    type=str,
    default=defaults.WASM_CONTRACT_FILENAME
    )


def main():
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Set arguments.
    args = Arguments.create(ARGS.parse_args())

    # Framework requirement: register arguments type.
    encoder.register_type(Arguments)

    # Framework requirement: initialise broker.
    mq.init_broker(args.network_id)

    # Execute workflow.
    workflow = get_workflow(args)
    workflow.run()


# Entry point.
if __name__ == '__main__':
    main()