from stests.core.cache import get_store
from stests.core.types.factory import create_contract_account
from stests.core.mq import dramatiq
from stests.generators.wg_100 import metadata



# Queue to which message will be dispatched.
_QUEUE = f"{metadata.ID}.phase_01.contract"



@dramatiq.actor(queue_name=_QUEUE, actor_name="create_contract_account")
def create_account(ctx, index):
    """Creates a smart contract related network account.
    
    """
    print(111)
    account = create_contract_account(index)

    return ctx, account


@dramatiq.actor(queue_name=_QUEUE, actor_name="cache_contract_account")
def cache_account(args):
    """Caches a smart contract related network account.
    
    """
    ctx, account = args

    cache_store = get_store()
    cache_store.append_account(ctx, account)

    return ctx, account
