import argparse

from beautifultable import BeautifulTable

from stests.cli.utils import get_table
from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("Lists set of registered networks.")


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    data = cache.infra.get_networks()

    # Set cols/rows.
    cols = ["Name", "Type", "Status"]
    rows = map(lambda i: [
        i.name,
        i.typeof.name,
        i.status.name,
    ], sorted(data, key=lambda i: i.index))

    # Set table.
    t = get_table(cols, rows)
    t.column_alignments['Name'] = BeautifulTable.ALIGN_LEFT
    t.column_alignments['Status'] = BeautifulTable.ALIGN_RIGHT

    # Render.
    print(t)


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
