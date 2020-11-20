import json
import subprocess

from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.utils import paths



# Method upon client to be invoked.
_CLIENT_METHOD = "get-block"


def execute(
    network: Network,
    node: Node,
    block_hash: str = None,
    ) -> str:
    """Queries a node for a block - returns latest block if hash is not provided.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param block_hash: Hash of block being pulled.

    :returns: Representation of a block within a node's state.

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

    return json.loads(cli_response.stdout)['result']['block']
