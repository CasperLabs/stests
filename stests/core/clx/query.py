from stests.core.clx.utils import get_client
from stests.core.domain import Account
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import RunContext
from stests.core.utils import defaults
from stests.core.utils import factory
from stests.core.utils import logger



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


def get_block_info(ctx: RunContext, bhash: str) -> int:
    """Queries network for information pertaining to a specific block.

    :param ctx: Contextual information passed along flow of execution.
    :param bhash: Hash of a block.
    :returns: Block information.

    """
    client = get_client(ctx)

    return client.showBlock(block_hash_base16=bhash, full_view=False)


def _get_last_block_hash(client):
    """Returns a chain's last block hash.
    
    """
    last_block_info = next(client.showBlocks(1))

    return last_block_info.summary.block_hash.hex()
