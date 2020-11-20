import requests

from stests.core.types.infra import Network
from stests.core.types.infra import Node



def execute(
    network: Network,
    node: Node,
    ) -> str:
    """Queries a node for it's current metrics.

    :param network: Target network being tested.
    :param node: Target node being tested.

    :returns: Representation of a node's metrics.

    """
    url = f"{node.url_rest}/metrics"
    response = requests.get(url)

    return response.content.decode("utf-8")
