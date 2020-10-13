from stests.chain.utils import execute_cli
from stests.chain.utils import DeployDispatchInfo
from stests.chain.api import set_deploy
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.events import EventType



# Method upon client to be invoked.
_CLIENT_METHOD = "put-deploy"

# Name of smart contract to dispatch & invoke.
_CONTRACT_FNAME = "transfer_to_account_u512.wasm"


@execute_cli(_CLIENT_METHOD, EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(info: DeployDispatchInfo, cp2: Account, amount: int) -> str:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param info: Information required when dispatching a deploy.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.

    :returns: Deploy hash.

    """
    return set_deploy.execute(
        info.network,
        info.node,
        info.dispatcher,
        _CONTRACT_FNAME,
        [
            "--session-arg", "amount:u512='1000000'",
            "--session-arg", f"target:account_hash='account-hash-{cp2.account_hash}'",
        ]
    )
