import json
import random
import subprocess

from stests.core.logging import log_event
from stests.chain.utils import execute_cli
from stests.chain.utils import DeployDispatchInfo
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.utils import paths
from stests.events import EventType


# Method upon client to be invoked.
_CLIENT_METHOD = "transfer"

# Maximum value of a transfer ID.
_MAX_TRANSFER_ID = (2 ** 63) - 1


@execute_cli(_CLIENT_METHOD, EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(info: DeployDispatchInfo, cp2: Account, amount: int, verbose: bool = True) -> str:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param info: Standard information required to dispatch deploy.
    :param cp2: Account information of counter party 2.
    :param amount: Amount (in motes) to be transferred.
    :param verbose: Flag inidcating whether event will be logged.
    :returns: Dispatched deploy hash.

    """
    binary_path = paths.get_path_to_client(info.network)
    cp1 = info.dispatcher

    cli_response = subprocess.run([
        binary_path, _CLIENT_METHOD,
        "--target-account", cp2.account_key,
        "--amount", str(amount),
        "--chain-name", info.network.chain_name,
        "--gas-price", str(info.gas_price),
        "--node-address", info.node_address,
        "--payment-amount", str(info.fee),
        "--secret-key", info.dispatcher.get_private_key_pem_filepath(),
        "--transfer-id", str(random.randint(1, _MAX_TRANSFER_ID)),
        "--ttl", str(info.time_to_live),
        ],
        stdout=subprocess.PIPE,
        )
    deploy_hash = json.loads(cli_response.stdout)['result']['deploy_hash']
    
    if verbose:
        log_event(
            EventType.WFLOW_DEPLOY_DISPATCHED,
            f"{info.node.address} :: {deploy_hash} :: transfer (native) :: {amount} CSPR :: from {cp1.account_key[:8]} -> {cp2.account_key[:8]} ",
            info.node,
            deploy_hash=deploy_hash,
            )

    return deploy_hash
