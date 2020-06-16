import argparse
import dataclasses
import typing

from stests.workflows.generators.utils import constants
from stests.workflows.generators.utils.args import get_argparser



@dataclasses.dataclass
class Arguments:
    """Custom generator arguments passed along chain of execution.
    
    """
    # Number of increments to apply to array.
    increments: int

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            increments='increments' in args and args.increments,
        )


# Set command line arguments.
ARGS = get_argparser(f"Executes simple node-rs deploy mock.")

# CLI argument: initial CLX balance.
ARGS.add_argument(
    "--increments",
    help="Increments deploy array count. Default=1",
    dest="increments",
    type=int,
    default=1
    )

