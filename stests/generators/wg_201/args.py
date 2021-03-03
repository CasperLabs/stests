import argparse
import dataclasses

from stests.core.utils import args_validator
from stests.generators.utils import constants
from stests.generators.utils.args import get_argparser



@dataclasses.dataclass
class Arguments:
    """Custom generator arguments passed along chain of execution.
    
    """
    # Amount to withdraw from auction bid (motes).
    amount: int

    # Ordinal identifier of validator.
    validator_index: int

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            amount='amount' in args and args.amount,
            validator_index='validator_index' in args and args.validator_index,
        )


# Set command line arguments.
ARGS = get_argparser(f"Dispatches an auction withdraw bid deploy.")

# CLI argument: bid amount (motes).
ARGS.add_argument(
    "--amount",
    help="Amount to withdraw from auction bid (motes).  Default=10,000,000.",
    dest="amount",
    type=int,
    default=int(1e7)
    )

# CLI argument: validator index.
ARGS.add_argument(
    "--validator",
    dest="validator_index",
    help="Validator index - index of validator withdrawing an auction bid.",
    type=args_validator.validate_node_index,
    )
