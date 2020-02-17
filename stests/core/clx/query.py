from stests.core.cache import NetworkIdentifier
from stests.core.clx.utils import get_client
from stests.core.domain import Account
from stests.core.domain import Block
from stests.core.domain import BlockStatus
from stests.core.domain import RunContext
from stests.core.utils import factory



def get_balance(ctx: RunContext, account: Account) -> int:
    """Returns a chain account balance.

    :param ctx: Contextual information passed along flow of execution.
    :param account: Account whose balance will be queried.

    :returns: Account balance.

    """
    client = get_client(ctx)
    try:
        balance = client.balance(
            address=account.public_key,
            block_hash=_get_last_block_hash(client)
            )
    except Exception as err:
        if "Value not found: \" Key::Account" in err.details:
            return 0
        raise err
    else:
        return balance


def get_block_info(network_id: NetworkIdentifier, bhash: str) -> Block:
    """Queries network for information pertaining to a specific block.

    :param ctx: Contextual information passed along flow of execution.
    :param bhash: Hash of a block.
    :returns: Block information.

    """
    client = get_client(network_id)
    info = client.showBlock(block_hash_base16=bhash, full_view=False)

    # print(info)

    return factory.create_block(
        bhash=bhash,
        deploy_cost_total=info.status.stats.deploy_cost_total,
        deploy_count=info.summary.header.deploy_count, 
        deploy_gas_price_avg=info.status.stats.deploy_gas_price_avg,
        rank=info.summary.header.rank,
        size_bytes=info.status.stats.block_size_bytes,
        timestamp=info.summary.header.timestamp,
        validator_id=info.summary.header.validator_public_key.hex()
        )


def get_block_deploys(network_id: NetworkIdentifier, bhash: str) -> Block:
    """Queries network for set of deploys associated with a specific block.

    :param ctx: Contextual information passed along flow of execution.
    :param bhash: Hash of a block.
    :returns: Block information.

    """
    client = get_client(network_id)
    info = client.showDeploys(block_hash_base16=bhash, full_view=False)


    # TODO: convert to domain type
    return info


def _get_last_block_hash(client):
    """Returns a chain's last block hash.
    
    """
    last_block_info = next(client.showBlocks(1))

    return last_block_info.summary.block_hash.hex()
