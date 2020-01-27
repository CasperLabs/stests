import argparse

from stests.core.utils.workflow import WorkflowContext
from stests.generators.wg_100 import defaults
from stests.generators.wg_100.args import Arguments
from stests.generators.wg_100.phase_01.workflow import factory



# Set workflow command line argument parser.
ARGS = Arguments.get_parser()

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

# Set workflow specific arguments.
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



# TODO: can streamline below boilerplate even further.

# Set workflow arguments.
args = Arguments.create(ARGS.parse_args())

# Set workflow execution context.
ctx = WorkflowContext.create(args)

# Set workflow.
workflow = factory.get_workflow(ctx, args)

# Execute.
workflow.run()
