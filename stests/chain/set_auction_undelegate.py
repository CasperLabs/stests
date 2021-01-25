from stests.chain import set_deploy
from stests.chain.utils import execute_cli
from stests.chain.utils import DeployDispatchInfo
from stests.core.types.chain import Account
from stests.events import EventType



# Method upon client to be invoked.
_CLIENT_METHOD = "put-deploy"

# Name of smart contract to dispatch & invoke.
_CONTRACT_FNAME = "undelegate.wasm"


@execute_cli(_CLIENT_METHOD, EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(info: DeployDispatchInfo, validator: Account, amount: int) -> str:
    """Submits a deploy revoking the delegation of an amount of tokens (in motes) from a validator.

    :param info: Information required when dispatching a deploy.
    :param validator: Account information of validator to whom a user is delegating stake.
    :param amount: Amount to submit to auction bid (motes).

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
            "--session-arg", f"validator:public_key='{validator.account_key}'",
        ]
    )
