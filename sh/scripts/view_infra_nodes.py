import argparse

from beautifultable import BeautifulTable

from stests.core import cache
from stests.core import factory
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env


# CLI argument parser.
ARGS = argparse.ArgumentParser("List set of nodes registered with a network.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# Table columns.
COLS = [
    ("ID", BeautifulTable.ALIGN_LEFT),
    ("Host:Port", BeautifulTable.ALIGN_LEFT),
    ("Type", BeautifulTable.ALIGN_LEFT),
]

def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id=factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        utils.log_warning(f"Network {args.network} is unregistered.")
        return
    data = cache.infra.get_nodes(network_id)
    if not data:
        utils.log_warning(f"Network {args.network} has no nodes.")
        return

    # Set cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: [
        i.label_index,
        f"{i.host}:{i.port_rpc}",
        i.typeof.name,
    ], sorted(data, key=lambda i: i.index))

    # Set table.
    t = utils.get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent

    # Render.
    print(t)
    print(f"{network_id.name} node count = {len(data)}")



# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
