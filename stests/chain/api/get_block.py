from jsonrpcclient import request

from stests.core.types.infra import Network
from stests.core.types.infra import Node



# Method upon client to be invoked.
_RPC_METHOD = "chain_get_block"


def execute(
    network: Network,
    node: Node,
    block_hash: str,
    ) -> str:
    """Queries a node for a block.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param block_hash: Hash of block being pulled.

    :returns: Representation of a block within a node's state.

    """
    response = request(node.url_rpc, _RPC_METHOD, block_hash=block_hash)

    return response.data.result['block']
