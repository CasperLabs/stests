import json
import subprocess

from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.utils import paths



# Method upon client to be invoked.
_CLIENT_METHOD = "get-state-root-hash"


def execute(
    network: Network,
    node: Node,
    block_hash: str = None,
    ) -> str:
    """Queries a node for it's current state root hash.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param block_hash: Hash of block for which state root hash is being returned.

    :returns: Current root state hash at a network node.

    """
    binary_path = paths.get_path_to_client(network)

    if block_hash:
        cli_response = subprocess.run([
            binary_path, _CLIENT_METHOD,
            "--node-address", node.url_rpc,
            "--block-identifier", block_hash,
            ],
            stdout=subprocess.PIPE,
            )  
    else:
        cli_response = subprocess.run([
            binary_path, _CLIENT_METHOD,
            "--node-address", node.url_rpc,
            ],
            stdout=subprocess.PIPE,
            )  

    return json.loads(cli_response.stdout)['result']['state_root_hash']
