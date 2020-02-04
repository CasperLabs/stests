import argparse
from dataclasses import dataclass
from dataclasses_json import dataclass_json

import dramatiq 

from stests.core import mq
from stests.core.types import GeneratorContext
from stests.core.utils import args_validator
from stests.generators.wg_100 import defaults
from stests.generators.wg_100 import metadata
from stests.generators.wg_100.phase_01 import orchestrator



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes {metadata.DESCRIPTION} workflow.")

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


@dataclass_json
@dataclass
class Arguments:
    """WG-100 generator execution arguments.
    
    """
    # Name of ERC20 token for which an auction is being simulated.
    token_name: str

    # Total amount of ERC20 token to be issued.
    token_supply: int

    # Number of user accounts to generate.
    user_accounts: int

    # Number of bids to submit per user.
    user_bids: int

    # Initial user account CLX balance.
    user_initial_clx_balance: int


    @staticmethod
    def create(args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return Arguments(
            token_name='token_name' in args and args.token_name,
            token_supply='token_supply' in args and args.token_supply,
            user_accounts='user_accounts' in args and args.user_accounts,
            user_bids='user_bids' in args and args.user_bids,
            user_initial_clx_balance='user_initial_clx_balance' in args and args.user_initial_clx_balance,
        )


args=ARGS.parse_args()

ctx = GeneratorContext.create(
    args=Arguments.create(args),
    network=args.network,
    node=args.node,
    run=args.run,
    typeof=metadata.TYPE    
    )

orchestrator.execute(ctx)
