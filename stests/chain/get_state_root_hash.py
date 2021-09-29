from stests.core.types.infra import Node



def execute(node: Node, block_hash: str = None) -> str:
    """Queries a node for it's current state root hash.

    :param node: Target node being tested.
    :param block_hash: Hash of block for which state root hash is being returned.

    :returns: Global state root hash at a network node.

    """
    # Map inputs to pycspr objects.
    node_client = node.as_pycspr_client

    state_root_hash: bytes = node_client.queries.get_state_root_hash()

    return state_root_hash.hex()
