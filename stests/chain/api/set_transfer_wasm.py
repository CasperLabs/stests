import subprocess
import typing

from stests.chain import constants
from stests.chain import utils
from stests.chain.api import set_deploy
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.events import EventType



# Name of smart contract to dispatch & invoke.
_CONTRACT_FNAME = "transfer_to_account.wasm"


def execute(
    network: Network,
    node: Node,
    cp1: Account,
    cp2: Account,
    amount: int,
    tx_ttl=constants.DEFAULT_TX_TIME_TO_LIVE,
    tx_fee=constants.DEFAULT_TX_FEE,
    tx_gas_price=constants.DEFAULT_TX_GAS_PRICE,
    ) -> typing.Tuple[str, float, int]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param network: Network to which transfer is being dispatched.
    :param node: Node to which transfer is being dispatched.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :param tx_ttl: Time to live before transaction processing is aborted.
    :param tx_fee: Transaction network fee.
    :param tx_gas_price: Network gas price.

    :returns: 3 member tuple -> (deploy_hash, dispatch_duration, dispatch_attempts)

    """
    return set_deploy(
        network=network,
        node=node,
        account=cp1,
        contract_fname=_CONTRACT_FNAME,
        tx_ttl=tx_ttl,
        tx_fee=tx_fee,
        tx_gas_price=tx_gas_price,
    )
