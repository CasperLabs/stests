import argparse

from beautifultable import BeautifulTable

from stests.cli.utils import get_table
from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger
from stests.core.orchestration import ExecutionAspect



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays summary information for a run.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: run type.
ARGS.add_argument(
    "run_type",
    help="Generator type - e.g. wg-100.",
    type=args_validator.validate_run_type,
    )

# CLI argument: run index.
ARGS.add_argument(
    "run_index",
    help="Run identifier, e.g. 1-100.",
    type=args_validator.validate_run_index,
    )



def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id = factory.create_network_id(args.network)
    data = cache.orchestration.get_info_list(network_id, args.run_type, args.run_index)
    if not data:
        logger.log("No run information found.")
        return

    # Set cols/rows.
    cols = ["Phase / Step", "Start Time", "Duration (s)", "Action", "Status"]
    rows = map(lambda i: [
        i.index_label,
        i.ts_start,
        i.tp_elapsed_label,
        i.step_label if i.step_label else '--'  ,      
        i.status.name,
    ], sorted(data, key=lambda i: i.index_label))

    # Set table.
    t = get_table(cols, rows)
    t.column_alignments['Phase / Step'] = BeautifulTable.ALIGN_LEFT
    t.column_alignments['Start Time'] = BeautifulTable.ALIGN_LEFT
    t.column_alignments['Duration (s)'] = BeautifulTable.ALIGN_RIGHT
    t.column_alignments['Action'] = BeautifulTable.ALIGN_RIGHT
    t.column_alignments['Status'] = BeautifulTable.ALIGN_RIGHT

    # Render.
    print(t)
    print(f"{network_id.name} - {args.run_type}  - Run {args.run_index}")



# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
