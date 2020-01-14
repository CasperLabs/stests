import json
import typing

from stests.core.utils.execution import ExecutionContext
from stests.core.utils import encoder



def do_set(ctx: ExecutionContext, key: str, data: typing.Any):
    """Executes redis.set command.
    
    :param ctx: Contextual information passed along the flow of execution.
    :param key: Key of item to be cached.
    :param data: Data to be cached.

    """
    print(data)
    as_json = json.dumps(encoder.encode(data), indent=4)

    ctx.services.cache.set(key, as_json)


def do_get(ctx: ExecutionContext, key: str) -> typing.Any:
    """Executes redis.get command.
    
    :param ctx: Contextual information passed along the flow of execution.
    :param key: Key of item to be cached.

    """
    as_json = ctx.services.cache.get(key)

    return encoder.decode(json.loads(as_json))
