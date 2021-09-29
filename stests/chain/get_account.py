import typing

from stests.core.types.infra import Node



def execute(node: Node, account_key: str, block_id: typing.Union[None, bytes, str, int] = None) -> str:
    """Queries a node for a block.

    :param node: Target node being tested.
    :param account_key: Key of account being pulled.
    :param block_id: Identifier of a finalised block.
    
    :returns: JSON representation of an on-chain account.

    """
    # Map inputs to pycspr objects.
    node_client = node.as_pycspr_client

    return node_client.queries.get_account_info(account_key, block_id)
