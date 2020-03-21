import argparse

from beautifultable import BeautifulTable

from stests.cli.utils import get_table
from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("Lists a network's client side contracts.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )


# Table columns.
COLS = [
    ("Network", BeautifulTable.ALIGN_LEFT),
    ("Hash", BeautifulTable.ALIGN_LEFT),
    ("Name", BeautifulTable.ALIGN_LEFT),
    ("Type", BeautifulTable.ALIGN_RIGHT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id=factory.create_network_id(args.network)
    if cache.infra.get_network(network_id) is None:
        logger.log_warning(f"Network {args.network} is unregistered.")
        return
    data = cache.infra.get_contracts(network_id)
    if not data:
        logger.log_warning(f"Network {args.network} has no registered contracts.")
        return

    # Set table cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: [
        network_id.name,
        i.hash,      
        i.name,      
        i.typeof.name,
    ], sorted(data, key=lambda i: i.typeof.name))

    # Set table.
    t = get_table(cols, rows, max_width=1080)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent    

    # Render.
    print(t)


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
