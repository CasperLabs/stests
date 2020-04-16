import typing

from stests.core.clx import parser
from stests.core.clx import utils
from stests.core.domain import Account
from stests.core.utils import logger



def get_account(src: typing.Any, account: Account, block_hash: str=None):
    """Returns on-chain account info.

    :param src: The source from which a node client will be instantiated.
    :param account: Account whose on-chain representation will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account info.

    """
    _, client = utils.get_client(src)

    q = client.queryState(
        block_hash or _get_last_block_hash(client),
        account.public_key,
        "",
        keyType="address"
        )

    return q.account


def get_account_balance(src: typing.Any, account: Account, block_hash: str = None) -> int:
    """Returns a chain account balance.

    :param src: The source from which a node client will be instantiated.
    :param account: Account whose balance will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account balance.

    """
    return get_account_balance_by_address(src, account.public_key, block_hash)


def get_account_balance_by_address(src: typing.Any, address: str, block_hash: str = None) -> int:
    """Queries account balance at a chain address.

    :param src: The source from which a node client will be instantiated.
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
            logger.log_warning(f"CHAIN :: get_account_balance :: account appears not to exist upon chain: address={address}")
            return 0
        raise err
    else:
        return balance


def get_account_named_keys(src: typing.Any, account: Account, block_hash: str=None):
    """Returns named keys associated with a chain account.

    :param src: The source from which a node client will be instantiated.
    :param account: Account whose on-chain representation will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account named keys.

    """
    a = get_account(src, account, block_hash)

    return a.named_keys


def get_block_info(src: typing.Any, block_hash: str, parse=True) -> typing.Dict:
    """Queries network for information pertaining to a specific block.

    :param src: The source from which a node client will be instantiated.
    :param block_hash: Hash of block against which query will be made.
    :param parse: Flag indicating whether to parse block info.

    :returns: Block info pulled from chain.

    """
    node, client = utils.get_client(src)
    info = client.showBlock(block_hash_base16=block_hash, full_view=False)

    return parser.parse_block_info(info) if parse else info


def get_deploy_info(src: typing.Any, deploy_hash: str, wait_for_processed: bool = True, parse=True) -> typing.Dict:
    """Queries node for a set of deploys associated with a specific block.

    :param src: The source from which a node client will be instantiated.
    :param deploy_hash: Hash of deploy for which query will be made.
    :param wait_for_processed: Flag indicating whether to block & await block processing.
    :param parse: Flag indicating whether to parse deploy info.

    :returns: Deploy info pulled from chain.

    """
    node, client = utils.get_client(src)
    info = client.showDeploy(deploy_hash, full_view=False, wait_for_processed=wait_for_processed)

    return parser.parse_deploy_info(info) if parse else info


def _get_last_block_hash(client) -> str:
    """Returns a chain's last block hash.
    
    """
    last_block_info = next(client.showBlocks(1))

    return last_block_info.summary.block_hash.hex()
