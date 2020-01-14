import dramatiq

from stests.core.cache import accessor as cache
from stests.core.types import factory as type_factory
from stests.generators.wg_100 import metadata



# Queue to which message will be dispatched.
_QUEUE = f"{metadata.ID}.phase_01.accounts"


@dramatiq.actor(queue_name=_QUEUE)
def create(ctx, account_type, account_id):
    """Creates an account to be used during simulation execution.
    
    """
    # Instantiate.
    account = type_factory.create_account(account_type, account_id)

    # Cache.
    cache.append_account(ctx, account)

    return ctx, account
