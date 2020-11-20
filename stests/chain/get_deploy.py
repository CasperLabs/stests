import json
import subprocess

from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.utils import paths



# Method upon client to be invoked.
_CLIENT_METHOD = "get-deploy"


def execute(
    network: Network,
    node: Node,
    deploy_hash: str = None,
    ) -> str:
    """Queries a node for a deploy.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param deploy_hash: Hash of deploy being pulled.

    :returns: Representation of a deploy within a node's state.

    """
    binary_path = paths.get_path_to_client(network)

    cli_response = subprocess.run([
        binary_path, _CLIENT_METHOD,
        "--node-address", node.url_rpc,
        deploy_hash,
        ],
        stdout=subprocess.PIPE,
        )    

    return json.loads(cli_response.stdout)['result']
