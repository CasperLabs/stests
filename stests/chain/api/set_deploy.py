import json
import subprocess
import typing

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
    dispatchee: Account,
    contract_fname: str, 
    session_args: list=[],
    tx_ttl=constants.DEFAULT_TX_TIME_TO_LIVE,
    tx_fee=constants.DEFAULT_TX_FEE,
    tx_gas_price=constants.DEFAULT_TX_GAS_PRICE,
    ) -> typing.Tuple[str, float, int]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param network: Network to which transfer is being dispatched.
    :param node: Node to which transfer is being dispatched.
    :param validator: Account information of validator submitting an auction bid.
    :param amount: Amount in motes to be transferred.
    :param tx_ttl: Time to live before transaction processing is aborted.
    :param tx_fee: Transaction network fee.
    :param tx_gas_price: Network gas price.

    :returns: 3 member tuple -> (deploy_hash, dispatch_duration, dispatch_attempts)

    """
    binary_path = paths.get_path_to_client(network)
    session_path = paths.get_path_to_contract(network, contract_fname)

    cli_response = subprocess.run([
        binary_path, _CLIENT_METHOD,
        "--chain-name", network.chain_name,
        "--gas-price", str(tx_gas_price),
        "--node-address", f"http://{node.address}",
        "--payment-amount", str(tx_fee),
        "--secret-key", dispatchee.get_private_key_pem_filepath(),
        "--session-path", session_path,
        "--ttl", str(tx_ttl),
        ] + session_args,
        stdout=subprocess.PIPE,
        )

    return json.loads(cli_response.stdout)['deploy_hash']
