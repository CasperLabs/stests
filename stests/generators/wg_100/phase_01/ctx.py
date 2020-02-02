import argparse
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils import encoder
from stests.core.utils.generator import GeneratorContext
from stests.core.utils.generator import GeneratorScope
from stests.generators.wg_100 import metadata



@dataclass_json
@dataclass
class Context(GeneratorContext):
    """WG-100 generator execution context information.
    
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
        :returns: Generator context information.

        """
        return Context(
            scope = GeneratorScope.create(metadata.TYPE, args),
            token_name = 'token_name' in args and args.token_name,
            token_supply = 'token_supply' in args and args.token_supply,
            user_accounts = 'user_accounts' in args and args.user_accounts,
            user_bids = 'user_bids' in args and args.user_bids,
            user_initial_clx_balance = 'user_initial_clx_balance' in args and args.user_initial_clx_balance,
        )


# Framework requirement: register context with encoder.
encoder.register_type(Context)
