import argparse
import dataclasses
import typing



@dataclasses.dataclass
class Arguments:
    """WG-100 generator execution arguments.
    
    """
    # Initial contract account CLX balance.
    contract_initial_clx_balance: int

    # Initial faucet account CLX balance.
    faucet_initial_clx_balance: int

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

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            contract_initial_clx_balance='contract_initial_clx_balance' in args and args.contract_initial_clx_balance,
            faucet_initial_clx_balance='faucet_initial_clx_balance' in args and args.faucet_initial_clx_balance,
            token_name='token_name' in args and args.token_name,
            token_supply='token_supply' in args and args.token_supply,
            user_accounts='user_accounts' in args and args.user_accounts,
            user_bids='user_bids' in args and args.user_bids,
            user_initial_clx_balance='user_initial_clx_balance' in args and args.user_initial_clx_balance,
        )
