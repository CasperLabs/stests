import argparse
import json

from beautifultable import BeautifulTable

from stests.core.utils.cli import get_table
from stests.core import cache
from stests.core import clx
from stests.core.utils import args_validator
from stests.core import factory
from stests.core.utils import logger
from stests.core.types.orchestration import ExecutionAspect



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays deploy information either pulled from chain or from stests cache.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: run type.
ARGS.add_argument(
    "deploy_hash",
    help="Deploy hash.",
    type=str,
    )

# Table columns.
COLS = [
    ("Deploy Property", BeautifulTable.ALIGN_LEFT),
    ("Value", BeautifulTable.ALIGN_LEFT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network_id = factory.create_network_id(args.network)
    node = _render_deploy(network_id, args.deploy_hash)
    _render_deploy_info(node or network_id, args.deploy_hash)


def _render_deploy(network_id, deploy_hash):
    """Renders cached deploy information.
    
    """
    raise NotImplementedError("TODO: remove")
    # Pull deploy either from run state or monitoring cache.
    deploy = cache.state.get_deploy(deploy_hash) or \
             cache.monitoring.get_deploy(network_id, deploy_hash)
    if not deploy:
        logger.log("No deploy information found.")
        return

    # Pull account/node.
    account = _get_deploy_account(network_id, deploy)
    node = _get_deploy_node(network_id, deploy)

    # Set cols/rows.
    cols = [i for i, _ in COLS]
    rows = []
    rows.append(("Network", network_id.name))
    rows.append(("Block", deploy.block_hash or "N/A"))
    rows.append(("Hash", deploy.hash))
    rows.append(("Status", deploy.status.name))
    rows.append(("Type", "N/A" if not deploy.typeof else deploy.typeof.name))
    # rows.append(("Cost", deploy_info["cost"]))
    rows.append(("Dispatch Node", node.address if node else "N/A"))
    rows.append(("Dispatch TimeStamp", deploy.dispatch_ts or "N/A"))
    rows.append(("Finalization TimeStamp", deploy.finalization_ts or "N/A"))
    rows.append(("Finalization Time (secs)", deploy.finalization_time or "N/A"))
    if deploy.is_from_run:
        rows.append(("Run Type", deploy.run_type))
        rows.append(("Run ID", deploy.label_run_index))
        rows.append(("Run Account ID", deploy.label_account_index))
        rows.append(("Run Account Key", account.public_key))

    # Set table.
    t = get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent    

    # Render.
    print(t)

    return node


def _get_deploy_account(network_id, deploy):
    """Returns account under which a deploy was dispatched.
    
    """
    if not deploy.is_from_run:
        return

    if deploy.account_index == 0:
        network = cache.infra.get_network(network_id)
        return network.faucet

    account_id = factory.create_account_id(
        deploy.account_index,
        network_id.name,
        deploy.run_index,
        deploy.run_type,
    )
    return cache.state1.get_account(account_id)


def _get_deploy_node(network_id, deploy):
    """Returns node to which a deploy was dispatched.
    
    """
    if not deploy.is_from_run:
        return

    node_id = factory.create_node_id(
        network_id,
        deploy.dispatch_node,
    )
    return cache.infra.get_node(node_id)


def _render_deploy_info(src, deploy_hash):
    """Renders on-chain deploy information.
    
    """
    deploy_info = clx.get_deploy_info(src, deploy_hash)
    if not deploy_info:
        return
    
    print("--------------------------------------------------------------------------------------------")
    print(json.dumps(deploy_info, indent=4))
    print("--------------------------------------------------------------------------------------------")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
