import argparse
import dataclasses
import typing

from stests.workflows.generators.utils.args import get_argparser
from stests.workflows.generators.wg_200 import constants



@dataclasses.dataclass
class Arguments:
    """WG-200 generator execution arguments.
    
    """
    # Initial faucet account CLX balance.
    faucet_initial_clx_balance: int

    # Number of times counters will be incremented.
    increments: int

    # Number of user accounts to generate.
    user_accounts: int

    # Initial user account CLX balance.
    user_initial_clx_balance: int

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            faucet_initial_clx_balance='faucet_initial_clx_balance' in args and args.faucet_initial_clx_balance,
            increments='increments' in args and args.increments,
            user_accounts='user_accounts' in args and args.user_accounts,
            user_initial_clx_balance='user_initial_clx_balance' in args and args.user_initial_clx_balance,
        )


# Set command line arguments.
ARGS = get_argparser(f"Executes {constants.DESCRIPTION} generator.")

# CLI argument: initial CLX balance.
ARGS.add_argument(
    "--faucet-initial-clx-balance",
    help=f"Initial CLX balance of faucet account. Default={constants.FAUCET_INITIAL_CLX_BALANCE}",
    dest="faucet_initial_clx_balance",
    type=int,
    default=constants.FAUCET_INITIAL_CLX_BALANCE
    )

# CLI argument: increments.
ARGS.add_argument(
    "--increments",
    help=f"Number of times counters will be incremented. Default={constants.INCREMENTS}",
    dest="increments",
    type=int,
    default=constants.INCREMENTS
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
