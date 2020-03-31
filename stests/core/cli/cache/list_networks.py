import argparse

from beautifultable import BeautifulTable

from stests.core.cli.utils import get_table
from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("Lists set of registered networks.")


# Table columns.
COLS = [
    ("Name", BeautifulTable.ALIGN_LEFT),
    ("Type", BeautifulTable.ALIGN_LEFT),
    ("Status", BeautifulTable.ALIGN_RIGHT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    data = cache.infra.get_networks()

    # Set cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: [
        i.name,
        i.typeof.name,
        i.status.name,
    ], sorted(data, key=lambda i: i.index))

    # Set table.
    t = get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent    

    # Render.
    print(t)


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
