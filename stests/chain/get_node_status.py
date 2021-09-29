from stests.core.types.infra import Node



def execute(node: Node,) -> str:
    """Queries a node for it's current status.

    :param node: Target node being tested.

    :returns: Representation of a node's status.

    """
    # Map inputs to pycspr objects.
    node_client = node.as_pycspr_client

    return node_client.queries.get_node_status()

