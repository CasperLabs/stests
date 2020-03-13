import argparse
import dataclasses
import typing



@dataclasses.dataclass
class Arguments:
    """WG-100 generator execution arguments.
    
    """
    # Initial faucet account CLX balance.
    faucet_initial_clx_balance: int

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
            user_accounts='user_accounts' in args and args.user_accounts,
            user_initial_clx_balance='user_initial_clx_balance' in args and args.user_initial_clx_balance,
        )
