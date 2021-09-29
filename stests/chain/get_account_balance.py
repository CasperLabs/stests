import json

from stests.core.types.infra import Node
from stests.core.utils import paths



def execute(
    node: Node,
    purse_uref: str,
    state_root_hash: str = None,
    ) -> int:
    """Queries account balance at a certain block height | hash.

    :param node: Target node being tested.
    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.

    :returns: Account balance.

    """
    # Map inputs to pycspr objects.
    node_client = node.as_pycspr_client

    return node_client.queries.get_account_balance(purse_uref, state_root_hash)
