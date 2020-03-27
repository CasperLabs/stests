import typing
from datetime import datetime

from stests.core.clx import utils
from stests.core.domain import Account
from stests.core.domain import Block
from stests.core.domain import BlockStatus
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
from stests.core.utils import logger

from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import MessageToJson


@utils.clx_op
def get_balance(src: typing.Union[ExecutionContext, NodeIdentifier], account: Account, block_hash: str = None) -> int:
    """Returns a chain account balance.

    :param src: The source from which a network node will be derived.
    :param account: Account whose balance will be queried.

    :returns: Account balance.

    """
    _, client = utils.get_client(src)
    try:
        balance = client.balance(
            address=account.public_key,
            block_hash=block_hash or get_last_block_hash(client)
            )
    except Exception as err:
        if "Failed to find base key at path" in err.details:
            return 0
        raise err
    else:
        return balance


@utils.clx_op
def get_block_by_node(node_id: NodeIdentifier, block_hash: str) -> typing.Dict:
    """Queries network for information pertaining to a specific block.

    :param node_id: A node identifier.
    :param block_hash: Hash of a block.

    :returns: 2 member tuple: (block info, block summary).

    """
    node, client = utils.get_client(node_id)

    return client.showBlock(block_hash_base16=block_hash, full_view=False)


@utils.clx_op
def get_deploys_by_node(node_id: NodeIdentifier, block_hash: str) -> typing.List[typing.Union[str, typing.Dict]]:
    """Queries node for a set of deploys associated with a specific block.

    :param node_id: A node identifier.
    :param block_hash: Hash of a block.

    :returns: 2 member tuple: (deploy hash, deploy info).

    """
    node, client = utils.get_client(node_id)

    deploys = client.showDeploys(block_hash_base16=block_hash, full_view=False)

    return ((i.deploy.deploy_hash.hex(), MessageToDict(i)) for i in deploys)


@utils.clx_op
def get_last_block_hash(client) -> str:
    """Returns a chain's last block hash.
    
    """
    last_block_info = next(client.showBlocks(1))

    return last_block_info.summary.block_hash.hex()


@utils.clx_op
def get_contract_hash(ctx: ExecutionContext, account: Account, dhash: str) -> str:
    """Returns hash of an on-chain contract.
    
    :param ctx: Execution context information.
    :param account: On-chain account under which contract was deployed.
    :param dhash: Hash of a previously processed deploy.

    :returns: Hash of on-chain contract.

    """
    _, client = utils.get_client(ctx)

    dinfo = client.showDeploy(dhash, wait_for_processed=True)
    bhash = dinfo.processing_results[0].block_info.summary.block_hash.hex()
    chash = utils.get_contract_hash(client, account, bhash, "counter")

    return chash