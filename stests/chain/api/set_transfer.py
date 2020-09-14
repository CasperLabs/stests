import subprocess

from stests.chain import constants
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node



# Method upon client to be invoked.
_CLIENT_METHOD = "transfer"


def execute(
    network: Network,
    node: Node,
    cp1: Account,
    cp2: Account,
    amount: int,
    tx_ttl=constants.DEFAULT_TX_TIME_TO_LIVE,
    tx_fee=constants.DEFAULT_TX_FEE,
    tx_gas_price=constants.DEFAULT_TX_GAS_PRICE,
    ) -> str:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param network: Network to which transfer is being dispatched.
    :param node: Node to which transfer is being dispatched.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :param tx_ttl: Time to live before transaction processing is aborted.
    :param tx_fee: Transaction network fee.
    :param tx_gas_price: Network gas price.

    :returns: deploy_hash.

    """
    cli_response = subprocess.run([
        constants.PATH_TO_BINARY, _CLIENT_METHOD,
        "--amount", str(amount),
        "--chain-name", network.chain_name,
        "--gas-price", str(tx_gas_price),
        "--node-address", f"http://{node.address}",
        "--payment-amount", str(tx_fee),
        "--secret-key", cp1.get_private_key_pem_filepath(),
        "--target-account", cp2.account_id,
        "--ttl", str(tx_ttl),
        ],
        stdout=subprocess.PIPE,
        )

    try:
        deploy_hash = cli_response.stdout.split(b'\n')[1]
    except Exception as err:
        # TODO: inspect error and decide correct course of action (e.g. discard or retries)
        raise err
    else:
        return str(deploy_hash)
