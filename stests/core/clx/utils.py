import typing

import casperlabs_client as pyclx

from stests.core import cache
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionRunInfo
from stests.core.utils import logger



def get_client(src: typing.Union[Node, NodeIdentifier, NetworkIdentifier, ExecutionRunInfo]) -> typing.Tuple[Node, pyclx.CasperLabsClient]:
    """Factory method to return a configured clabs client and the node with which it is associated.

    :param src: The source from which a network node will be derived.

    :returns: A configured clabs client ready for use.
    
    """
    # Set node. 
    if isinstance(src, Node):
        node = src
    elif isinstance(src, NodeIdentifier):
        node = cache.infra.get_node(src)
    elif isinstance(src, NetworkIdentifier):
        node = cache.infra.get_node_by_network_id(src)
    elif isinstance(src, ExecutionRunInfo):
        node = cache.infra.get_node_by_run_context(src)
    else:
        raise ValueError("Cannot derive node from input source.")
    if not node:
        raise ValueError("Network nodeset is empty, therefore cannot dispatch a deploy.")

    logger.log(f"PYCLX :: connecting to node :: {node.network}:N-{str(node.index).zfill(4)} :: {node.host}:{node.port}")

    # TODO: get node id / client ssl cert.
    return node, pyclx.CasperLabsClient(
        host=node.host,
        port=node.port,
    )


def clx_op(func: typing.Callable) -> typing.Callable:
    """Decorator over deploy operations.
    
    :param func: Inner function being decorated.

    :returns: Wrapped function.

    """
    def wrapper(*args, **kwargs):
        # Pre log.
        messages = {
            "get_block": lambda args: f"bhash={args[-1]}",
            "get_deploys": lambda args: f"bhash={args[-1]}",
            "get_balance": lambda args: f"pbk={args[-1].public_key}",
        }
        try:
            message = messages[func.__name__]
        except KeyError:
            logger.log(f"PYCLX :: {func.__name__} :: executing ...")
        else:
            logger.log(f"PYCLX :: {func.__name__} :: {message(args)}")

        try:
            return func(*args, **kwargs)
        except Exception as err:
            logger.log_error(f"PYCLX :: {err}")
            raise err

    return wrapper
