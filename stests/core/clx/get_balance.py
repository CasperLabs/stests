from stests.core.clx.utils import get_client_from_ctx
from stests.core.domain import Account
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import RunContext
from stests.core.utils import defaults
from stests.core.utils import factory
from stests.core.utils import logger



def execute(ctx: RunContext, account: Account) -> int:
    """Queries network for an account balance.

    :param ctx: Contextual information passed along flow of execution.
    :param account: Account whose balance will be queried.
    :returns: Account balance.

    """
    client = get_client_from_ctx(ctx)
    try:
        balance = client.balance(
            address=account.public_key,
            block_hash=get_last_block_hash(client)
            )
    except Exception as err:
        if "Value not found: \" Key::Account" in err.details:
            return 0
        raise err
    else:
        return balance


def get_last_block_hash(client):
    """Returns last blck hash by querying a node.
    
    """
    last_block_info = next(client.showBlocks(1))

    return last_block_info.summary.block_hash.hex()
