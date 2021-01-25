from stests.chain import set_deploy
from stests.chain.utils import execute_cli
from stests.chain.utils import DeployDispatchInfo
from stests.core.logging import log_event
from stests.core.types.chain import Account
from stests.events import EventType



# Method upon client to be invoked.
_CLIENT_METHOD = "put-deploy"

# Name of smart contract to dispatch & invoke.
_CONTRACT_FNAME = "delegate.wasm"


@execute_cli(_CLIENT_METHOD, EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(info: DeployDispatchInfo, validator: Account, amount: int, verbose: bool = True) -> str:
    """Submits a deploy delegating an amount of tokens (in motes) to a validator for staking purposes.

    :param info: Information required when dispatching a deploy.
    :param validator: Account information of validator to whom a user is delegating stake.
    :param amount: Amount to submit to auction bid (motes).
    :param verbose: Flag inidcating whether event will be logged.

    :returns: Deploy hash.

    """
    delegator = info.dispatcher

    deploy_hash = set_deploy.execute(
        info.network,
        info.node,
        info.dispatcher,
        _CONTRACT_FNAME,
        [
            "--session-arg", f"amount:u512='{amount}'",
            "--session-arg", f"delegator:public_key='{delegator.account_key}'",
            "--session-arg", f"validator:public_key='{validator.account_key}'",
        ]
    )

    if verbose:
        log_event(
            EventType.WFLOW_DEPLOY_DISPATCHED,
            f"{info.node.address} :: {deploy_hash} :: auction (delegate) :: {amount} CSPR :: from {delegator.account_key[:8]} -> {validator.account_key[:8]} ",
            info.node,
            deploy_hash=deploy_hash,
            )

    return deploy_hash
