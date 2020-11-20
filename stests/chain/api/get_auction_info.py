import json
import subprocess

from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.utils import paths



# Method upon client to be invoked.
_CLIENT_METHOD = "get-auction-info"


def execute(
    network: Network,
    node: Node,
    ) -> int:
    """Queries account balance at a certain block height | hash.

    :param network: Target network being tested.
    :param node: Target node being tested.

    :returns: On-chain auction information.

    """
    binary_path = paths.get_path_to_client(network)

    cli_response = subprocess.run([
        binary_path, _CLIENT_METHOD,
        "--node-address", node.url_rpc,
        ],
        stdout=subprocess.PIPE,
        )    

    return json.loads(cli_response.stdout)['result']
