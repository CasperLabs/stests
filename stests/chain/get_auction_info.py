from stests.core.types.infra import Node
from stests.core.utils import paths



def execute(node: Node) -> int:
    """Queries account balance at a certain block height | hash.

    :param node: Target node being tested.
    :returns: On-chain auction information.

    """
    # Map inputs to pycspr objects.
    node_client = node.as_pycspr_client

    return node_client.queries.get_auction_info()
