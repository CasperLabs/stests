import argparse

from beautifultable import BeautifulTable

from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionAspect
from stests.core.utils import args_validator
from stests.core.utils import cli as utils



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
    help="Run identifier.",
    type=args_validator.validate_run_index,
    )


# Table columns.
COLS = [
    ("Phase / Step", BeautifulTable.ALIGN_LEFT),
    ("Execution Start Time", BeautifulTable.ALIGN_LEFT),
    ("Execution End Time", BeautifulTable.ALIGN_LEFT),
    ("Duration (s)", BeautifulTable.ALIGN_RIGHT),
    ("Deploys", BeautifulTable.ALIGN_RIGHT),
    ("Action", BeautifulTable.ALIGN_RIGHT),
    ("Status", BeautifulTable.ALIGN_RIGHT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id = factory.create_network_id(args.network)
    data = cache.orchestration.get_info_list(network_id, args.run_type, args.run_index)
    if not data:
        utils.log("No run information found.")
        return

    # Set deploy counts.
    keys, counts = cache.orchestration.get_deploy_count_list(network_id, args.run_type, args.run_index)
    keys = [i.split(":") for i in keys]
    keys = [f"{i[2]}.{i[4]}" if i[4] != "-" else i[2] for i in keys]
    counts = dict(zip(keys, counts))

    # Sort data.
    data = sorted(data, key=lambda i: i.label_index)

    # Set cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: _get_row(i, counts), data)

    # Set table.
    t = utils.get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent    

    # Render.
    print(t)
    print(f"{network_id.name} - {args.run_type}  - Run {args.run_index}")


def _get_row(i, counts):
    """Returns table row data.
    
    """
    return [
        i.label_index,
        i.ts_start,
        "--" if not i.ts_end else i.ts_end,
        i.label_tp_elapsed,
        counts.get(i.label_index.strip(), 0),
        i.step_label if i.step_label else '--',      
        i.status.name,
    ]


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
