import subprocess

from stests.core.client import constants
from stests.core.client import utils
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.infra import Network



# Method upon client to be invoked.
_CLIENT_METHOD = "get-deploy"


def execute(
    network: Network,
    node: Node,
    deploy_hash: str,
    ) -> str:
    """Dispatches a transaction to a node upon test network.
    
    :param network: Target network being tested.
    :param node: Target node being tested.
    :param deploy_hash: Hexadecimal representation of dispatched transaction hash.

    :returns: Hexadecimal representation of dispatched transaction hash.

    """
    # TODO: http | https protocol derivation

    response = subprocess.run([
        constants.PATH_TO_BINARY, _CLIENT_METHOD,
        deploy_hash,
        "--node-address", f"http://{node.address}"
        ],
        stdout=subprocess.PIPE,
        )

    return response.stdout
