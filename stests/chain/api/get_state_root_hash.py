from jsonrpcclient import request

from stests.core.types.infra import Network
from stests.core.types.infra import Node



def execute(
    network: Network,
    node: Node,
    ) -> str:
    """Queries a node for it's current state root hash.

    :param network: Target network being tested.
    :param node: Target node being tested.

    :returns: A node's current root state hash.

    """
    response = request(node.url_rpc, "chain_get_block")

    return response.data.result['block']['header']['state_root_hash']
