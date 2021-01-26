import argparse

from beautifultable import BeautifulTable

from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionAspect
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays summary information for a run.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: run type.
ARGS.add_argument(
    "--type",
    default="wg-100",
    dest="run_type",
    help="Generator type - e.g. wg-100.",
    type=args_validator.validate_run_type,
    )

# CLI argument: run index.
ARGS.add_argument(
    "--run",
    default=1,
    dest="run_index",
    help="Run identifier.",
    type=args_validator.validate_run_index,
    )


# Table columns.
COLS = [
    ("Phase / Step", BeautifulTable.ALIGN_LEFT),
    ("Deploys", BeautifulTable.ALIGN_RIGHT),
    ("Duration (s)", BeautifulTable.ALIGN_RIGHT),
    ("Execution Start Time", BeautifulTable.ALIGN_RIGHT),
    ("Execution End Time", BeautifulTable.ALIGN_RIGHT),
    ("Action", BeautifulTable.ALIGN_RIGHT),
    ("Status", BeautifulTable.ALIGN_RIGHT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Set run data.
    network_id = factory.create_network_id(args.network)
    data = cache.orchestration.get_info_list(network_id, args.run_type, args.run_index)
    if not data:
        utils.log("No run information found.")
        return
    
    # Set sorted data.
    data = sorted(data, key=lambda i: i.label_index)

    # Set deploy counts.
    keys, counts = cache.orchestration.get_deploy_count_list(network_id, args.run_type, args.run_index)
    keys = [i.split(":") for i in keys]
    keys = [f"{i[3]}.{i[5]}" if i[5] != "-" else i[3] for i in keys]
    counts = dict(zip(keys, counts))

    # Set table.
    t = utils.get_table(
        [i for i, _ in COLS], 
        map(lambda i: _get_row(i, counts), data),
        )
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent    

    # Render.
    print(t)
    print("--------------------------------------------------------------------------------------------------------------------")
    print(f"{network_id.name} - {args.run_type}  - Run {args.run_index}")
    print("--------------------------------------------------------------------------------------------------------------------")


def _get_row(i, counts):
    """Returns table row data.
    
    """
    return [
        i.label_index,
        counts.get(i.label_index.strip(), 0),
        i.label_tp_elapsed,
        str(i.ts_start).split(" ")[1],
        "--" if not i.ts_end else str(i.ts_end).split(" ")[1],
        i.step_label if i.step_label else '--',      
        i.status.name,
    ]


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
