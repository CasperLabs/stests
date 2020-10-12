import argparse
import dataclasses

from stests.orchestration.generators.utils import constants
from stests.orchestration.generators.utils.args import get_argparser



@dataclasses.dataclass
class Arguments:
    """Custom generator arguments passed along chain of execution.
    
    """
    # Percentage (i.e. rate) of POS reward alloocated to delegators.
    delegation_rate: int

    # Bid amount (motes).
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
ARGS = get_argparser(f"Submits a bid to the validator auction.")

# CLI argument: bid amount (motes).
ARGS.add_argument(
    "--amount",
    help="Motes per transfer. Default=1000000",
    dest="amount",
    type=int,
    default=int(1e8)
    )

# CLI argument: bid delegation rate.
ARGS.add_argument(
    "--rate",
    help="Percentage (i.e. rate) of POS reward alloocated to delegators.",
    dest="delegation_rate",
    type=int,
    default=125
    )
