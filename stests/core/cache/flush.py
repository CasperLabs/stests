from stests.core.cache.utils import flushcache
from stests.core.domain import RunContext


@flushcache
def flush_run(ctx: RunContext):
    """Flushes previous run information.
    
    """
    yield ["run-account"] + ctx.keypath
    yield ["run-deploy"] + ctx.keypath
    yield ["run-event"] + ctx.keypath
    yield ["run-transfer"] + ctx.keypath
