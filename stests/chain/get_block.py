import typing

from stests.core.types.infra import Node



def execute(node: Node, block_id: typing.Union[None, bytes, str, int] = None) -> str:
    """Queries a node for a block - returns latest block if hash is not provided.

    :param node: Target node being tested.
    :param block_id: Identifier of a finalised block.

    :returns: Representation of a block within a node's state.

    """
    # Map inputs to pycspr objects.
    node_client = node.as_pycspr_client

    return node_client.queries.get_block(block_id)
