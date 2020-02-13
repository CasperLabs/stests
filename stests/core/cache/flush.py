from stests.core.cache.keyspace import get_key
from stests.core.cache.utils import flushcache
from stests.core.domain import RunContext



@flushcache
def flush_run(ctx: RunContext):
    """Flushes previous run information.
    
    """
    return get_key(ctx)
