import argparse

from beautifultable import BeautifulTable

from stests.core import cache
from stests.core import factory
from stests.core.utils import args_validator
from stests.core.utils import cli as utils


# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays set of registered networks.")


# Table columns.
COLS = [
    ("Name", BeautifulTable.ALIGN_LEFT),
    ("Type", BeautifulTable.ALIGN_LEFT),
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
    ], sorted(data, key=lambda i: i.index))

    # Set table.
    t = utils.get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent    

    # Render.
    print(t)


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
