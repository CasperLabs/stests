from stests.core.cache.keyspace import get_key
from stests.core.cache.utils import encache
from stests.core.domain import Account
from stests.core.domain import AccountTransfer
from stests.core.domain import Deploy
from stests.core.domain import Network
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.domain import RunEvent



@encache
def set_account(ctx: RunContext, account: Account):
    """Encaches domain object: Account.
    
    """
    key = f"{get_key(ctx)}:{get_key(account)}"

    return key, account


@encache
def set_account_transfer(ctx: RunContext, transfer: AccountTransfer):
    """Encaches domain object: AccountTransfer.
    
    """
    key = f"{get_key(ctx)}:{get_key(transfer)}"

    return key, transfer


@encache
def set_deploy(ctx: RunContext, deploy: Deploy):
    """Encaches domain object: Deploy.
    
    """
    key = f"{get_key(ctx)}:{get_key(deploy)}"

    return key, deploy


@encache
def set_network(network: Network):
    """Encaches domain object: Network.
    
    """
    key = f"global.network:{network.name}"

    return key, network


@encache
def set_node(node: Node):
    """Encaches domain object: Node.
    
    """
    key = f"global.node:{node.network}:N-{str(node.index).zfill(4)}"

    return key, node


@encache
def set_run_context(ctx: RunContext):
    """Encaches domain object: RunContext.
    
    """
    key = f"{get_key(ctx)}:context"

    return key, ctx


@encache
def set_event(ctx: RunContext, evt: RunEvent):
    """Encaches domain object: RunEvent.
    
    """
    key = f"{get_key(ctx)}:{get_key(evt)}"

    return key, evt
