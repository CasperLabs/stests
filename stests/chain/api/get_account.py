from jsonrpcclient import request

from stests.chain.api.get_state_root_hash import execute as get_state_root_hash
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node



# Method upon client to be invoked.
_RPC_METHOD = "state_get_item"


def execute(
    network: Network,
    node: Node,
    account_hash: str,
    state_root_hash=None,
    ) -> str:
    """Queries a node for a block.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param account: Off-chain account information.
    :param state_root_hash: State root hash at a node within target network.
    
    :returns: Representation of an account within a node's state.

    """
    state_root_hash = state_root_hash or get_state_root_hash(network, node)
    response = request(node.url_rpc, _RPC_METHOD, 
        state_root_hash=state_root_hash,
        key=f"account-hash-{account_hash}",
        path=[]
        )

    return response.data.result['stored_value']
