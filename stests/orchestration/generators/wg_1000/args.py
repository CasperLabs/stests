import argparse
import dataclasses

from stests.orchestration.generators.utils import constants
from stests.orchestration.generators.utils.args import get_argparser



@dataclasses.dataclass
class Arguments:
    """Custom generator arguments passed along chain of execution.
    
    """
    # Number of 'deploys' to apply to array.
    deploys: int

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            deploys='deploys' in args and args.deploys,
        )


# Set command line arguments.
ARGS = get_argparser(f"Executes simple node-rs deploy mock.")

# CLI argument: initial CLX balance.
ARGS.add_argument(
    "--deploys",
    help="Increments deploy array count. Default=1",
    dest="deploys",
    type=int,
    default=1
    )

