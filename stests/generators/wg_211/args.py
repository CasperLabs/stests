import argparse
import dataclasses

from stests import chain
from stests.generators.utils import constants
from stests.generators.utils.args import get_argparser



@dataclasses.dataclass
class Arguments:
    """Custom generator arguments passed along chain of execution.
    
    """
    # Amount to submit for auction bid (motes).
    amount: int

    # Count of delegators to simulate.
    delegators: int

    @property
    def amount_to_fund(self):
        """Amount that each delegator will be pre-funded with."""
        return self.amount + (3 * chain.DEFAULT_TX_FEE)

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            amount='amount' in args and args.amount,
            delegators='delegators' in args and args.delegators,
        )


# Set command line arguments.
ARGS = get_argparser("Tests the auction contract by submitting batches of delegation/undelegation requests.")

# CLI argument: bid amount (motes).
ARGS.add_argument(
    "--amount",
    help="Amount to delegate/undelegate (motes).  Default=1,000,000.",
    dest="amount",
    type=int,
    default=int(1e6)
    )

# CLI argument: bid amount (motes).
ARGS.add_argument(
    "--delegators",
    help="Number of delegators to simulate.  Default=10.",
    dest="delegators",
    type=int,
    default=int(10)
    )
