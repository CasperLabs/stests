import subprocess

from stests.chain import constants
from stests.chain import contracts
from stests.chain import utils
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.infra import Network
from stests.events import EventType


# Method upon client to be invoked.
_CLIENT_METHOD = "put-deploy"


@utils.execute_cli(_CLIENT_METHOD, EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(
    account: Account,
    network: Network,
    node: Node,
    contract_fname = None,
    tx_ttl=constants.DEFAULT_TX_TIME_TO_LIVE,
    tx_fee=constants.DEFAULT_TX_FEE,
    tx_gas_price=constants.DEFAULT_TX_GAS_PRICE,
    ) -> str:
    """Dispatches a transaction to a node upon test network.
    
    :param account: Account signing transaction to be dispatched.
    :param network: Target network being tested.
    :param node: Target node being tested.
    :param contract_fname: Name of smart contract being executed.
    :param tx_ttl: Time to live before transaction processing is aborted.
    :param tx_fee: Transaction network fee.
    :param tx_gas_price: Network gas price.

    :returns: 3 member tuple -> (deploy_hash, dispatch_duration, dispatch_attempts)

    """
    cli_response = subprocess.run([
        constants.PATH_TO_BINARY, _CLIENT_METHOD,
        "--chain-name", network.chain_name or "",
        "--gas-price", str(tx_gas_price),
        "--node-address", f"http://{node.address}",
        "--payment-amount", str(tx_fee),
        "--secret-key", account.get_private_key_pem_filepath,
        "--session-path", contracts.get_contract_path(contract_fname),
        "--ttl", str(tx_ttl),
        ],
        stdout=subprocess.PIPE,
        )
    
    return cli_response.stdout.split(b'\n')[1]
