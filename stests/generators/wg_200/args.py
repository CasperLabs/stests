import argparse
import dataclasses

from stests.core.utils import args_validator
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

    # Ordinal identifier of validator.
    validator_index: int

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            amount='amount' in args and args.amount,
            delegation_rate='delegation_rate' in args and args.delegation_rate,
            validator_index='validator_index' in args and args.validator_index,
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

# CLI argument: validator index.
ARGS.add_argument(
    "--validator",
    dest="validator_index",
    help="Validator index - index of validator submitting an auction bid.",
    type=args_validator.validate_node_index,
    )
