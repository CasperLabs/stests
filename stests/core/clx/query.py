import typing

import casperlabs_client

from stests.core.clx import utils
from stests.core.logging import log_event
from stests.core.types.chain import Account
from stests.events import EventType



def get_account_info(src: typing.Any, account_id: str, block_hash: str=None, parse=True):
    """Returns on-chain account info.

    :param src: The source from which a node client will be instantiated.
    :param account_id: Identifier of account whose on-chain representation will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account info.

    """
    q = get_state(src, block_hash, account_id, "address", "")

    return utils.parse_chain_info(q.account) if parse else q.account


def get_account_balance(src: typing.Any, account_id: str, block_hash: str = None) -> int:
    """Queries account balance at a chain address.

    :param src: The source from which a node client will be instantiated.
    :param account_id: Identifier of account whose balance will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account balance.

    """
    node, client = utils.get_client(src)

    try:
        balance = client.balance(
            address=account_id,
            block_hash=block_hash or _get_last_block_hash(client)
            )
    except Exception as err:
        if err and err.details:
            if "StatusCode.INVALID_ARGUMENT" in err.details:
                log_event(EventType.MONIT_ACCOUNT_NOT_FOUND, f"account_id={account_id}", node)
                return 0
        raise err
    else:
        return balance


def get_named_keys(src: typing.Any, account: Account, block_hash: str=None, filter_keys: typing.List[str]=[]):
    """Returns named keys associated with a chain account.

    :param src: The source from which a node client will be instantiated.
    :param account: Account whose on-chain representation will be queried.
    :param block_hash: Hash of block against which query will be made.
    :param filter_keys: Keys of interest.

    :returns: Account named keys.

    """
    a = get_account_info(src, account.account_id, block_hash, parse=False)

    keys = a.named_keys
    if filter_keys:
        keys = [i for i in keys if i.name in filter_keys]

    return keys


def get_block_info(src: typing.Any, block_hash: str, parse=True) -> typing.Dict:
    """Queries network for information pertaining to a specific block.

    :param src: The source from which a node client will be instantiated.
    :param block_hash: Hash of block against which query will be made.
    :param parse: Flag indicating whether to parse block info.

    :returns: Block info pulled from chain.

    """
    _, client = utils.get_client(src)

    try:
        info = client.showBlock(block_hash_base16=block_hash, full_view=False)
    except casperlabs_client.InternalError as err:
        if err and err.details:
            if "StatusCode.NOT_FOUND" in err.details:
                return None
            if "StatusCode.INVALID_ARGUMENT" in err.details:
                raise ValueError("Block hash format is invalid")
        raise err
    else:
        return utils.parse_chain_info(info) if parse else info    


def get_deploy_info(src: typing.Any, deploy_hash: str, wait_for_processed: bool = True, parse=True) -> typing.Dict:
    """Queries node for a set of deploys associated with a specific block.

    :param src: The source from which a node client will be instantiated.
    :param deploy_hash: Hash of deploy for which query will be made.
    :param wait_for_processed: Flag indicating whether to block & await block processing.
    :param parse: Flag indicating whether to parse deploy info.

    :returns: Deploy info pulled from chain.

    """
    _, client = utils.get_client(src)

    try:
        info = client.showDeploy(deploy_hash, full_view=False, wait_for_processed=wait_for_processed)
    except casperlabs_client.InternalError as err:
        if err and err.details:
            if "StatusCode.NOT_FOUND" in err.details:
                return None
            if "StatusCode.INVALID_ARGUMENT" in err.details:
                raise ValueError("Deploy hash format is invalid")
        raise err
    else:
        return utils.parse_chain_info(info) if parse else info


def _get_last_block_hash(client) -> str:
    """Returns a chain's last block hash.
    
    """
    last_block_info = next(client.showBlocks(1))

    return last_block_info.summary.block_hash.hex()


def get_state(src: typing.Any, block_hash: str, key: str, key_type: str, path: str):
    """Queries node for a item within global state.

    :param src: The source from which a node client will be instantiated.
    :param block_hash: Hash of block for which query will be made.
    :param key: Name of key against which to issue a query.
    :param key_type: Type of key.
    :param path: Path within global state data.

    :returns: Global state info pulled from chain.

    """    
    _, client = utils.get_client(src)

    return client.queryState(
        block_hash or _get_last_block_hash(client),
        key,
        path,
        key_type,
        )
