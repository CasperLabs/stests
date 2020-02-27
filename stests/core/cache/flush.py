import typing

from stests.core.cache.utils import flushcache
from stests.core.domain import NetworkIdentifier
from stests.core.domain import RunContext



@flushcache
def flush_run(ctx: RunContext) -> typing.Generator:
    """Flushes previous run information.

    :param ctx: Generator run contextual information.

    :returns: A generator of keypaths to be flushed.
    
    """
    for collection in [
        "run-account",
        "run-context",
        "run-deploy",
        "run-event",
        "run-step",
        "run-step-deploy",
        "run-step-lock",
        "run-transfer",
    ]:
        yield [
            collection,
            ctx.network,
            ctx.run_type,
            f"R-{str(ctx.run).zfill(3)}",
            "*"
        ]


@flushcache
def flush_network(network_id: NetworkIdentifier) -> typing.Generator:
    """Flushes previous run information.

    :param network_id: A network identifier.

    :returns: A generator of keypaths to be flushed.
    
    """
    yield ["network", network_id.name]

    for collection in [
        "network-block",
        "network-deploy",
        "network-node",

        "run-account",
        "run-context",
        "run-deploy",
        "run-event",
        "run-step",
        "run-step-deploy",
        "run-step-lock",
        "run-transfer",
    ]:
        yield [
            collection,
            network_id.name,
            "*"
        ]
