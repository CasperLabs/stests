import json
import subprocess

from stests.chain.get_state_root_hash import execute as get_state_root_hash
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.utils import paths



# Method upon client to be invoked.
_CLIENT_METHOD = "get-balance"


def execute(
    network: Network,
    node: Node,
    purse_uref: str,
    state_root_hash: str = None,
    ) -> int:
    """Queries account balance at a certain block height | hash.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.

    :returns: Account balance.

    """
    binary_path = paths.get_path_to_client(network)
    state_root_hash = state_root_hash or get_state_root_hash(network, node)

    cli_response = subprocess.run([
        binary_path, _CLIENT_METHOD,
        "--node-address", node.url_rpc,
        "--state-root-hash", state_root_hash,
        "--purse-uref", purse_uref
        ],
        stdout=subprocess.PIPE,
        )    

    try:
        return int(json.loads(cli_response.stdout)['result']['balance_value'])
    except json.decoder.JSONDecodeError:
        return None
