import argparse

from beautifultable import BeautifulTable

from stests.cli.utils import get_table
from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("List set of nodes registered with a network.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id=factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        logger.log_warning(f"Network {args.network} is unregistered.")
        return
    data = cache.infra.get_nodes(network_id)
    if not data:
        logger.log_warning(f"Network {args.network} has no nodes.")
        return

    # Set cols/rows.
    cols = ["ID", "Host:Port", "Type", "Status"]
    rows = map(lambda i: [
        i.index_label,
        f"{i.host}:{i.port}",
        i.typeof.name,
        i.status.name,
    ], sorted(data, key=lambda i: i.index))

    # Set table.
    t = get_table(cols, rows)
    t.column_alignments['Host:Port'] = BeautifulTable.ALIGN_LEFT

    # Render.
    print(t)
    print(f"{network_id.name} node count = {len(data)}")



# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
