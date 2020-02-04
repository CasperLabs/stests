import argparse
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.types import GeneratorContext
from stests.core.types import NetworkReference
from stests.core.utils import encoder



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


@dataclass_json
@dataclass
class Context(GeneratorContext):
    args: Arguments

    @classmethod
    def create(cls, args: Arguments, network: str, node: int, run: int, typeof: str):
        """Simple factory method.

        """
        return Context(
            args=args,
            network=NetworkReference.create(network),
            node=node,
            typeof=typeof.upper(),
            run=run
        )


# Framework requirement in support of serialisation scenarios.
encoder.register_type(Context)
