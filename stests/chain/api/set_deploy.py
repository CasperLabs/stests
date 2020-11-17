import json
import subprocess

from stests.chain import constants
from stests.chain import utils
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.utils import paths
from stests.events import EventType



# Method upon client to be invoked.
_CLIENT_METHOD = "put-deploy"


def execute(
    network: Network,
    node: Node,
    dispatcher: Account,
    contract_fname: str,
    session_args: list=[],
    tx_ttl=constants.DEFAULT_TX_TIME_TO_LIVE,
    tx_fee=constants.DEFAULT_TX_FEE,
    tx_gas_price=constants.DEFAULT_TX_GAS_PRICE,
    ) -> str:
    """Dispatches a signed deploy to target test network.

    :param dispatcher: Account information of entity dispatching a deploy.
    :param contract_fname: Smart contract file name being dispatched.

    :param network: Network to which transfer is being dispatched.
    :param node: Node to which transfer is being dispatched.
    :param tx_ttl: Time to live before transaction processing is aborted.
    :param tx_fee: Transaction network fee.
    :param tx_gas_price: Network gas price.

    :returns: Deploy hash.

    """
    binary_path = paths.get_path_to_client(network)
    session_path = paths.get_path_to_contract(network, contract_fname)

    cli_response = subprocess.run([
        binary_path, _CLIENT_METHOD,
        "--chain-name", network.chain_name,
        "--gas-price", str(tx_gas_price),
        "--node-address", node.url_rpc,
        "--payment-amount", str(tx_fee),
        "--secret-key", dispatcher.get_private_key_pem_filepath(),
        "--session-path", session_path,
        "--ttl", str(tx_ttl),
        ] + session_args,
        stdout=subprocess.PIPE,
        )

    return json.loads(cli_response.stdout)['result']['deploy_hash']
