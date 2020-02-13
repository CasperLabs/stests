from stests.core.cache.keyspace import get_key
from stests.core.cache.stores import get_store
from stests.core.cache.utils import flush_namespace
from stests.core.domain import RunContext
from stests.core.utils import encoder



def _do_flush(instance):
    """Sink function to flush instances of domain types.
    
    """
    with get_store() as store:
        flush_namespace(store, get_key(instance))


# Flush run information.
def flush_run(ctx: RunContext):
    _do_flush(ctx)

