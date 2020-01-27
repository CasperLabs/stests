from stests.core.cache.stores import StoreType
from stests.core.cache.stores import redis
from stests.core.cache.stores import stub
from stests.core.utils.workflow import WorkflowContext


# Map: Cache store type -> factory.
FACTORIES = {
    StoreType.REDIS: redis,
    StoreType.STUB: stub
}


def get_store(ctx: WorkflowContext, store_type: StoreType = StoreType.REDIS):
    """Returns a cache store ready to be used as a state persistence & flow control mechanism.

    :param ctx: Contextual information passed along the flow of execution.
    :param store_type: Type of store to be instantiated.
    :returns: A cache store.

    """
    try:
        factory = FACTORIES[store_type]
    except KeyError:
        raise NotImplementedError(f"{store_type} cache store is unsupported")

    return factory.get_store(ctx.network_id)
