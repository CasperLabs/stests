from stests.chain import set_deploy
from stests.chain.utils import execute_cli
from stests.chain.utils import DeployDispatchInfo
from stests.core.logging import log_event
from stests.events import EventType



# Method upon client to be invoked.
_CLIENT_METHOD = "put-deploy"

# Name of smart contract to dispatch & invoke.
_CONTRACT_FNAME = "withdraw_bid.wasm"


@execute_cli(_CLIENT_METHOD, EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(info: DeployDispatchInfo, amount: int, verbose: bool = True) -> str:
    """Withdraws a bid from network's validator slot auction contract.

    :param info: Information required when dispatching a deploy.
    :param amount: Amount to withdraw from auction bid (motes).
    :param verbose: Flag inidcating whether event will be logged.

    :returns: Deploy hash.

    """
    deploy_hash = set_deploy.execute(
        info.network,
        info.node,
        info.dispatcher,
        _CONTRACT_FNAME,
        [
            "--session-arg", f"amount:u512='{amount}'",
            "--session-arg", f"public_key:public_key='{info.dispatcher.account_key}'",
        ]
    )

    if verbose:
        log_event(
            EventType.WFLOW_DEPLOY_DISPATCHED,
            f"{info.node.address} :: {deploy_hash} :: auction withdraw-bid :: {amount} CSPR :: by node {info.node.index} ",
            info.node,
            deploy_hash=deploy_hash,
            )

    return deploy_hash 
