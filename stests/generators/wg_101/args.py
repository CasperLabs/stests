import argparse
import dataclasses

from stests import chain
from stests.generators.utils import constants
from stests.generators.utils.args import get_argparser



@dataclasses.dataclass
class Arguments:
    """Custom generator arguments passed along chain of execution.
    
    """
    # Number of transfers to dispatch. Default=1000.
    transfers: int

    # Motes per transfer to transfer.
    amount: int

    # Controls number of on-the-fly accounts to be generated during the run.
    accounts: int

    @property
    def faucet_initial_balance(self):
        """Initial faucet account CSPR balance."""
        return  (self.transfers * self.amount) + (((2 * self.transfers) + 1) * chain.DEFAULT_TX_FEE)


    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            accounts='accounts' in args and args.accounts,
            transfers='transfers' in args and args.transfers,
            amount='amount' in args and args.amount,
        )


# Set command line arguments.
ARGS = get_argparser(f"Native transfers generator.")

# CLI argument: # transfers to dispatch.
ARGS.add_argument(
    "--transfers",
    help="Number of transfers to dispatch. Default=100",
    dest="transfers",
    type=int,
    default=100
    )

# CLI argument: motes per transfer.
ARGS.add_argument(
    "--amount",
    help="Motes per transfer. Default=10000000000",
    dest="amount",
    type=int,
    default=int(1e10)
    )

# CLI argument: # transfers to dispatch.
ARGS.add_argument(
    "--accounts",
    help="Number of target accounts to create on the fly. If set to 0 then each target account is unique.  If set to 1 then a single target account is created.",
    dest="accounts",
    type=int,
    default=0
    )
