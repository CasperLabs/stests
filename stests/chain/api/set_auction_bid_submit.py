from stests.chain.api import set_deploy
from stests.chain.utils import execute_cli
from stests.chain.utils import DeployDispatchInfo
from stests.events import EventType



# Method upon client to be invoked.
_CLIENT_METHOD = "put-deploy"

# Name of smart contract to dispatch & invoke.
_CONTRACT_FNAME = "add_bid.wasm"


@execute_cli(_CLIENT_METHOD, EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(info: DeployDispatchInfo, amount: int, delegation_rate: int) -> str:
    """Submits a bid to network's validator slot auction contract.

    :param info: Information required when dispatching a deploy.
    :param amount: Amount to submit to auction bid (motes).
    :param delegation_rate: Percentage (i.e. rate) of POS reward alloocated to delegators.

    :returns: Deploy hash.

    """
    return set_deploy.execute(
        info.network,
        info.node,
        info.dispatcher,
        _CONTRACT_FNAME,
        [
            "--session-arg", f"amount:u512='{amount}'",
            "--session-arg", f"delegation_rate:u64='{delegation_rate}'",
        ]
    )
