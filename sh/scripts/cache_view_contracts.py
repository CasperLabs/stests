import argparse

from beautifultable import BeautifulTable

from stests.core import cache
from stests.core import factory
from stests.core.utils import cli as utils
from stests.core.utils import args_validator
from stests.core.utils import env



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays information related to test smart contracts registered with stests & stored on-chain.")

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
    ("Network", BeautifulTable.ALIGN_LEFT),
    ("Type", BeautifulTable.ALIGN_LEFT),
    ("Name/Slot", BeautifulTable.ALIGN_LEFT),
    ("Hash", BeautifulTable.ALIGN_RIGHT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id=factory.create_network_id(args.network)
    if cache.infra.get_network(network_id) is None:
        utils.log_warning(f"Network {args.network} is unregistered.")
        return
    data = cache.infra.get_named_keys(network_id)
    if not data:
        utils.log_warning(f"Network {args.network} has no registered contracts.")
        return

    # Sort data.
    data = sorted(data, key=lambda i: f"{i.contract_type}.{i.name}")

    # Set table cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: [
        network_id.name,
        i.contract_type,
        i.name,      
        i.hash,      
    ], data)

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
