import typing

from stests.chain import constants
from stests.chain import utils
from stests.chain.api import set_deploy
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.events import EventType



# Method upon client to be invoked.
_CLIENT_METHOD = "put-deploy"

# Name of smart contract to dispatch & invoke.
_CONTRACT_FNAME = "delegate.wasm"


@utils.execute_cli(_CLIENT_METHOD, EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(
    network: Network,
    node: Node,
    delegator: Account,
    validator: Account,
    amount: int,
    tx_ttl=constants.DEFAULT_TX_TIME_TO_LIVE,
    tx_fee=constants.DEFAULT_TX_FEE,
    tx_gas_price=constants.DEFAULT_TX_GAS_PRICE,
    ) -> str:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param delegator: Account information of entity delegating stake to a validator.
    :param validator: Account information of validator to whom a user is delegating stake.
    :param amount: Amount to submit to auction bid (motes).

    :param network: Network to which transfer is being dispatched.
    :param node: Node to which transfer is being dispatched.
    :param tx_ttl: Time to live before transaction processing is aborted.
    :param tx_fee: Transaction network fee.
    :param tx_gas_price: Network gas price.

    :returns: Deploy hash.

    """
    return set_deploy.execute(
        network,
        node,
        delegator,
        _CONTRACT_FNAME,
        [
            "--session-arg", f"amount:u512='{amount}'",
            "--session-arg", f"validator:public_key='{validator.account_id}'",
        ]
    )
