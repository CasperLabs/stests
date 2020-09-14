import subprocess
import typing

from stests.chain import constants
from stests.chain import utils
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.infra import Network



# Method upon client to be invoked.
_CLIENT_METHOD = "list-deploys"


def execute(network: Network, node: Node) -> typing.List[str]:
    """Queries test network for a set of previously dispatched deploys.
    
    :param network: Target network being tested.
    :param node: Target node being tested.

    :returns: List of previously dispatched deploys.

    """
    response = subprocess.run([
        constants.PATH_TO_BINARY, _CLIENT_METHOD,
        "--node-address", f"http://{node.address}"
        ],
        stdout=subprocess.PIPE,
        )

    return response.stdout
