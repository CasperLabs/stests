import typing
from datetime import datetime

from google.protobuf.json_format import MessageToDict

from stests.core.clx import parser
from stests.core.clx import utils
from stests.core.domain import Account
from stests.core.domain import Block
from stests.core.domain import BlockStatus
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
from stests.core.utils import logger



def get_account(client, account: Account, block_hash: str=None):
    """Returns on-chain account info.

    :param client: Client instance.
    :param account: Account whose on-chain representation will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account info.

    """
    block_hash or _get_last_block_hash(client)
    q = client.queryState(block_hash, account.public_key, "", keyType="address")

    return q.account


def get_account_named_keys(client, account: Account, block_hash: str=None):
    """Returns named keys associated with a chain account.

    :param client: Client instance.
    :param account: Account whose on-chain representation will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account named keys.

    """
    a = get_account(client, account, block_hash)

    return a.named_keys


def get_balance(src: typing.Union[ExecutionContext, NetworkIdentifier, NodeIdentifier], account: Account, block_hash: str = None) -> int:
    """Returns a chain account balance.

    :param src: The source from which a network node will be derived.
    :param account: Account whose balance will be queried.

    :returns: Account balance.

    """
    return get_balance_by_address(src, account.public_key, block_hash)


def get_balance_by_address(src: typing.Union[ExecutionContext, NetworkIdentifier, NodeIdentifier], address: str, block_hash: str = None) -> int:
    """Queries account balance at a chain address.

    :param src: The source from which a network node will be derived.
    :param address: Address whose balance will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account balance.

    """
    _, client = utils.get_client(src)
    try:
        balance = client.balance(
            address=address,
            block_hash=block_hash or _get_last_block_hash(client)
            )
    except Exception as err:
        if "Failed to find base key at path" in err.details:
            logger.log_warning(f"CHAIN :: get_balance :: account appears not to exist upon chain: address={address}")
            return 0
        raise err
    else:
        return balance


def get_block_info(src: typing.Union[NetworkIdentifier, NodeIdentifier], block_hash: str, parse=True) -> typing.Dict:
    """Queries network for information pertaining to a specific block.

    :param src: The source from which a network node will be derived.
    :param block_hash: Hash of a block.
    :param parse: Flag indicating whether to parse block info.

    :returns: 2 member tuple: (block info, block summary).

    """
    node, client = utils.get_client(src)
    info = client.showBlock(block_hash_base16=block_hash, full_view=False)

    return parser.parse_block_info(info) if parse else info


def get_deploy_info(src: typing.Union[NetworkIdentifier, NodeIdentifier], deploy_hash: str, wait_for_processed: bool = True, parse=True) -> typing.Dict:
    """Queries node for a set of deploys associated with a specific block.

    :param src: The source from which a network node will be derived.
    :param deploy_hash: Hash of a deploy.

    :returns: Deploy info pulled from chain.

    """
    node, client = utils.get_client(src)
    info = client.showDeploy(deploy_hash, full_view=False, wait_for_processed=wait_for_processed)

    return parser.parse_deploy_info(info) if parse else info


def get_deploy_info_list_by_node_and_block(node_id: NodeIdentifier, block_hash: str) -> typing.List[typing.Union[str, typing.Dict]]:
    """Queries node for a set of deploys associated with a specific block.

    :param node_id: A node identifier.
    :param block_hash: Hash of a block.

    :returns: 2 member tuple: (deploy hash, deploy info).

    """
    node, client = utils.get_client(node_id)

    deploys = client.showDeploys(block_hash_base16=block_hash, full_view=False)

    return ((i.deploy.deploy_hash.hex(), parser.parse_deploy_info(i)) for i in deploys)


def _get_last_block_hash(client) -> str:
    """Returns a chain's last block hash.
    
    """
    last_block_info = next(client.showBlocks(1))

    return last_block_info.summary.block_hash.hex()

