import json
import subprocess

from stests.chain.utils import execute_cli
from stests.chain.utils import DeployDispatchInfo
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.utils import paths
from stests.events import EventType



# Method upon client to be invoked.
_CLIENT_METHOD = "transfer"


@execute_cli(_CLIENT_METHOD, EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(info: DeployDispatchInfo, cp2: Account, amount: int) -> str:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param info: Information required when dispatching a deploy.
    :param cp2: Account information of counter party 2.
    :param amount: Amount (in motes) to be transferred.

    :param info: Information required to dispatch node request.

    :returns: Deploy hash.

    """
    binary_path = paths.get_path_to_client(info.network)

    cli_response = subprocess.run([
        binary_path, _CLIENT_METHOD,
        "--target-account", cp2.account_key,
        "--amount", str(amount),
        "--chain-name", info.network.chain_name,
        "--gas-price", str(info.gas_price),
        "--node-address", info.node_address,
        "--payment-amount", str(info.fee),
        "--secret-key", info.dispatcher.get_private_key_pem_filepath(),
        "--ttl", str(info.time_to_live),
        ],
        stdout=subprocess.PIPE,
        )
    
    return json.loads(cli_response.stdout)['result']['deploy_hash']
