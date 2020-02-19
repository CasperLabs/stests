from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.cache.utils import encache1
from stests.core.domain import Account
from stests.core.domain import Block
from stests.core.domain import Transfer
from stests.core.domain import Deploy
from stests.core.domain import Network
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.domain import RunEvent



@encache1
def set_account(ctx: RunContext, account: Account):
    """Encaches domain object: Account.
    
    """
    return [
        "account",
        ctx.network_name,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        str(account.index).zfill(6)
    ], account


@encache1
def set_block(network_id: NetworkIdentifier, block: Block):
    """Encaches domain object: Block.
    
    """
    return [
        "block",
        network_id.name,
        f"{str(block.timestamp)}.{block.bhash}"
    ], block


@encache1
def set_deploy(ctx: RunContext, deploy: Deploy):
    """Encaches domain object: Deploy.
    
    """
    return [
        "deploy",
        ctx.network_name,
        ctx.run_type,
        ctx.run_index,
        deploy.ts_dispatched,
        deploy.dhash
    ], deploy


@encache1
def set_network(network: Network):
    """Encaches domain object: Network.
    
    """
    return [
        "network",
        network.name,
    ], network


@encache1
def set_node(node: Node):
    """Encaches domain object: Node.
    
    """
    return [
        "node",
        node.network,
        f"N-{str(node.index).zfill(4)}"
    ], node


@encache1
def set_run(ctx: RunContext):
    """Encaches domain object: RunContext.
    
    """
    return [
        "run",
        ctx.network_name,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}"
    ], ctx


@encache1
def set_run_event(ctx: RunContext, evt: RunEvent):
    """Encaches domain object: RunEvent.
    
    """
    return [
        "run_event",
        ctx.network_name,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        evt.timestamp,
        evt.event
    ], evt


@encache1
def set_transfer(ctx: RunContext, transfer: Transfer):
    """Encaches domain object: Transfer.
    
    """
    return [
        "transfer",
        ctx.network_name,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        transfer.asset.lower(),
        transfer.dhash
    ], transfer
