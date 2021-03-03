import argparse
import dataclasses

from stests.generators.utils import constants
from stests.generators.utils.args import get_argparser



@dataclasses.dataclass
class Arguments:
    """Custom generator arguments passed along chain of execution.
    
    """
    # Percentage (i.e. rate) of POS reward alloocated to delegators.
    delegation_rate: int

    # Amount to submit to auction bid (motes).
    amount: int

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            delegation_rate='delegation_rate' in args and args.delegation_rate,
            amount='amount' in args and args.amount,
        )


# Set command line arguments.
ARGS = get_argparser(f"Dispatches an auction submit bid deploy.")

# CLI argument: bid amount (motes).
ARGS.add_argument(
    "--amount",
    help="Amount to submit to auction bid (motes).  Default=100,000,000.",
    dest="amount",
    type=int,
    default=int(1e8)
    )

# CLI argument: bid delegation rate.
ARGS.add_argument(
    "--rate",
    help="Percentage (i.e. rate) of POS reward alloocated to delegators.  Default=125",
    dest="delegation_rate",
    type=int,
    default=2
    )
