import subprocess

from stests.chain import constants
from stests.chain import utils
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.infra import Network
from stests.core.utils import paths



# Method upon client to be invoked.
_CLIENT_METHOD = "get-deploy"


def execute(network: Network, node: Node, deploy_hash: str) -> str:
    """Dispatches a transaction to a node upon test network.
    
    :param network: Target network being tested.
    :param node: Target node being tested.
    :param deploy_hash: Hexadecimal representation of dispatched transaction hash.

    :returns: Hexadecimal representation of dispatched transaction hash.

    """
    binary_path = paths.get_path_to_client(network)

    response = subprocess.run([
        binary_path, _CLIENT_METHOD,
        deploy_hash,
        "--node-address", f"http://{node.address}",
        ],
        stdout=subprocess.PIPE,
        )

    return response.stdout
