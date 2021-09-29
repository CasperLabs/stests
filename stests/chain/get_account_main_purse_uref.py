from stests.chain.get_account import execute as get_account
from stests.core.types.infra import Node
from stests.core.types.infra import Network



def execute(
    network: Network,
    node: Node,
    account_key: str,
    state_root_hash: str = None,
    ) -> int:
    """Returns main purse uref for an account.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param account_key: Key of account being pulled.
    :param state_root_hash: State root hash at a node within target network.

    :returns: Account main purse uref.

    """
    # Map inputs to pycspr objects.
    node_client = node.as_pycspr_client

    # Query chain to pull main purse uref.
    uref = node_client.queries.get_account_main_purse_uref(account_key, state_root_hash)

    return uref.as_string()
