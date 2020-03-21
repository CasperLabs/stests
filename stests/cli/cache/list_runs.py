import argparse

from beautifultable import BeautifulTable

from stests.cli.utils import get_table
from stests.core import cache
from stests.core.orchestration import ExecutionAspect
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays summary information for all runs.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: run type.
ARGS.add_argument(
    "--run-type",
    help=f"Run type - e.g. wg-100.",
    dest="run_type",
    type=args_validator.validate_run_type,
    )


# Table columns.
COLS = [
    ("Type", BeautifulTable.ALIGN_LEFT),
    ("ID", BeautifulTable.ALIGN_LEFT),
    ("Start Time", BeautifulTable.ALIGN_LEFT),
    ("Duration (s)", BeautifulTable.ALIGN_RIGHT),
    ("Status", BeautifulTable.ALIGN_RIGHT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id = factory.create_network_id(args.network)
    data = cache.orchestration.get_info_list(network_id, args.run_type)
    data = [i for i in data if i.aspect == ExecutionAspect.RUN]
    if not data:
        logger.log("No run information found.")
        return    

    # Sort data.
    data = sorted(data, key=lambda i: f"{i.run_type}.{i.index_label}")

    # Set cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: [
        i.run_type,
        i.index_label.strip(),
        i.ts_start,
        i.tp_elapsed_label,
        i.status_label.strip()
    ], data)

    # Set table.
    t = get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent  

    # Render.
    print(t)
    print(f"total runs = {len(data)}")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
