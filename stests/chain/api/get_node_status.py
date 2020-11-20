from jsonrpcclient import request

from stests.core.types.infra import Network
from stests.core.types.infra import Node



# Method upon client to be invoked.
_RPC_METHOD = "info_get_status"


def execute(
    network: Network,
    node: Node,
    ) -> str:
    """Queries a node for it's current status.

    :param network: Target network being tested.
    :param node: Target node being tested.

    :returns: Representation of a node's status.

    """
    response = request(node.url_rpc, _RPC_METHOD)

    return response.data.result

