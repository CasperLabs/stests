import argparse
import statistics

from beautifultable import BeautifulTable

from stests.core.cli.utils import get_table
from stests.core import cache
from stests.core.domain import DeployStatus
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
    help="Run identifier.",
    type=args_validator.validate_run_index,
    )

# Table columns.
COLS = [
    ("#", BeautifulTable.ALIGN_LEFT),
    ("Deploy Hash", BeautifulTable.ALIGN_LEFT),
    ("Type", BeautifulTable.ALIGN_RIGHT),
    ("Status", BeautifulTable.ALIGN_RIGHT),
    ("Node", BeautifulTable.ALIGN_RIGHT),
    ("Account", BeautifulTable.ALIGN_RIGHT),
    ("Dispatch Timestamp", BeautifulTable.ALIGN_RIGHT),
    ("Finalization Time", BeautifulTable.ALIGN_RIGHT),
    ("Block Hash", BeautifulTable.ALIGN_RIGHT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id = factory.create_network_id(args.network)
    data = cache.state.get_deploys(network_id, args.run_type, args.run_index)
    if not data:
        logger.log("No run deploys found.")
        return

    # Render views.
    _render_table(args, network_id, data)
    _render_finalization_stats(data)


def _render_table(args, network_id, data):
    # Sort data.
    data = sorted(data, key=lambda i: i.dispatch_ts)

    # Set table cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: [
        data.index(i) + 1,
        i.deploy_hash,      
        i.typeof.name,
        i.status.name,      
        i.dispatch_node,
        i.account_index,
        i.dispatch_ts,
        i.label_finalization_time,
        i.block_hash or "--"
    ], data)

    # Set table.
    t = get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent    

    # Render.
    print(t)
    print(f"{network_id.name} - {args.run_type}  - Run {args.run_index}")


def _render_finalization_stats(data):
    """Renders finalization stats.
    
    """
    times = [i.finalization_time for i in data if i.finalization_time]
    if not times:
        return

    maxima = max(times)
    minima = min(times)
    avg = statistics.mean(times)
    stdev = statistics.stdev(times)
    variance = statistics.variance(times)

    print(f"Finalized = {len(times)} :: %={int((len(times) / len(data)) * 100)} :: Avg={format(avg, '.3f')}s :: Max={format(maxima, '.3f')}s :: Min={format(minima, '.3f')}s :: Variance={format(variance, '.3f')}s :: Std Dev= {format(stdev, '.3f')}s")

# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
