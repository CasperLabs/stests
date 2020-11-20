import argparse
import dataclasses

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

    @classmethod
    def create(cls, args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.

        """
        return cls(
            transfers='transfers' in args and args.transfers,
            amount='amount' in args and args.amount,
        )


# Set command line arguments.
ARGS = get_argparser(f"Wasm based transfers generator - wasm is dispatched with each transfer.")

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
    help="Motes per transfer. Default=100000000",
    dest="amount",
    type=int,
    default=int(1e8)
    )

