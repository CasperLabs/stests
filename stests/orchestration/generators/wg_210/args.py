import argparse
import dataclasses

from stests.orchestration.generators.utils import constants
from stests.orchestration.generators.utils.args import get_argparser



@dataclasses.dataclass
class Arguments:
    """Custom generator arguments passed along chain of execution.
    
    """
    # Amount to withdraw from auction bid (motes).
    amount: int

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            amount='amount' in args and args.amount,
        )


# Set command line arguments.
ARGS = get_argparser(f"Submits a deploy delegating an amount of tokens (in motes) to a validator for staking purposes.")

# CLI argument: bid amount (motes).
ARGS.add_argument(
    "--amount",
    help="Amount to delegate (motes).  Default=1,000,000.",
    dest="amount",
    type=int,
    default=int(1e6)
    )
