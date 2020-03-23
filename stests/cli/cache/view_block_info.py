import argparse
import json

from beautifultable import BeautifulTable

from stests.cli.utils import get_table
from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays deploy information pulled from chain.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: run type.
ARGS.add_argument(
    "block_hash",
    help="Block hash.",
    type=str,
    )

# Table columns.
COLS = [
    ("Block Property", BeautifulTable.ALIGN_LEFT),
    ("Value", BeautifulTable.ALIGN_LEFT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Destructure args.
    network_id = factory.create_network_id(args.network)

    # Pull monitoring data.
    block = cache.monitoring.get_block(network_id, args.block_hash)
    block_info = cache.monitoring.get_block_info(network_id, args.block_hash)
    if not block or not block_info:
        logger.log("No block information found.")
        return

    # Set cols/rows.
    cols = [i for i, _ in COLS]
    rows = []
    rows.append(("Network", network_id.name))
    rows.append(("Hash", block.hash))
    rows.append(("Deploy Cost (Total)", block.deploy_cost_total))
    rows.append(("Deploy Count", block.deploy_count))
    rows.append(("Gas Price (Avg)", block.deploy_gas_price_avg))
    rows.append(("Size (bytes)", block.size_bytes))
    rows.append(("Rank", block.m_rank))
    rows.append(("Rank-J", block.j_rank))
    rows.append(("Status", block.status.name))
    rows.append(("Timestamp", block.timestamp))

    # Set table.
    t = get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent    

    # Render.
    print(t)
    print(json.dumps(block_info, indent=4))
    print("-----------------------------------------------------------------------------------------------")
    print(f"{network_id.name} - {args.block_hash}")    
    print("-----------------------------------------------------------------------------------------------")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
