import json
import subprocess

from stests.chain.get_state_root_hash import execute as get_state_root_hash
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.utils import paths



# Method upon client to be invoked.
_CLIENT_METHOD = "query-state"


def execute(
    network: Network,
    node: Node,
    account_key: str,
    state_root_hash=None,
    ) -> str:
    """Queries a node for a block.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param account_key: Key of account being pulled.
    :param state_root_hash: State root hash at a node within target network.
    
    :returns: JSON representation of an on-chain account.

    """
    binary_path = paths.get_path_to_client(network)
    state_root_hash = state_root_hash or get_state_root_hash(network, node)

    cli_response = subprocess.run([
        binary_path, _CLIENT_METHOD,
        "--node-address", node.url_rpc,
        "--state-root-hash", state_root_hash,
        "--key", account_key
        ],
        stdout=subprocess.PIPE,
        )    

    return json.loads(cli_response.stdout)['result']
