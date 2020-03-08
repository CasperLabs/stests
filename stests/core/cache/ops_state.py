import random
import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.ops_infra import get_network
from stests.core.cache.ops_infra import get_nodes
from stests.core.cache.utils import cache_op
from stests.core.domain import *
from stests.core.orchestration import *
from stests.core.utils import factory



@cache_op(StorePartition.STATE, StoreOperation.FLUSH)
def flush_by_network(network_id: NetworkIdentifier) -> typing.Generator:
    """Flushes network specific monitoring information.

    :param network_id: A network identifier.

    :returns: A generator of keypaths to be flushed.
    
    """
    yield ["account", network_id.name, "*"]
    yield ["deploy", network_id.name, "*"]
    yield ["transfer", network_id.name, "*"]
        

@cache_op(StorePartition.STATE, StoreOperation.FLUSH)
def flush_by_run(ctx: ExecutionRunInfo) -> typing.Generator:
    """Flushes previous run information.

    :param ctx: Generator run contextual information.

    :returns: A generator of keypaths to be flushed.
    
    """
    for collection in [
        "account",
        "deploy",   
        "transfer",
    ]:
        yield [
            collection,
            ctx.network,
            ctx.run_type,
            f"R-{str(ctx.run_index).zfill(3)}",
            "*"
        ]


@cache_op(StorePartition.STATE, StoreOperation.GET)
def get_account(account_id: AccountIdentifier) -> Account:
    """Decaches domain object: Account.

    :param account_id: An account identifier.

    :returns: A cached account.

    """
    return [
        "account",
        account_id.run.network.name,
        account_id.run.type,
        f"R-{str(account_id.run.index).zfill(3)}",
        f"{str(account_id.index).zfill(6)}"
    ]


def get_account_by_run(ctx: ExecutionRunInfo, index: int) -> Account:
    """Decaches domain object: Account.
    
    :param ctx: Generator run contextual information.
    :param index: Run specific account index. 

    :returns: A cached account.

    """
    return get_account(factory.create_account_id(
        index,
        ctx.network,
        ctx.run_index,
        ctx.run_type
        ))


def get_run_deploy(dhash: str) -> Deploy:
    """Decaches domain object: Deploy.
    
    :param dhash: A deploy hash.

    :returns: A run deploy.

    """    
    deploys = get_run_deploys(dhash)

    return deploys[-1] if deploys else None


@cache_op(StorePartition.STATE, StoreOperation.GET)
def get_run_deploys(dhash: str) -> typing.List[Deploy]:
    """Decaches collection of domain objects: Deploy.
    
    :param dhash: A deploy hash.

    :returns: List of matching deploys.

    """    
    return [f"deploy*{dhash}*"]


def get_run_transfer(dhash: str) -> Transfer:
    """Decaches domain object: Transfer.
    
    :param dhash: A deploy hash.

    :returns: A run deploy.

    """    
    transfers = get_run_transfers(dhash)

    return transfers[-1] if transfers else None


@cache_op(StorePartition.STATE, StoreOperation.GET)
def get_run_transfers(dhash: str) -> typing.List[Transfer]:
    """Decaches collection of domain objects: Transfer.
    
    :param dhash: A deploy hash.

    :returns: Matched transfers.

    """    
    return [f"transfer*{dhash}*"]


@cache_op(StorePartition.STATE, StoreOperation.SET)
def set_run_account(account: Account) -> typing.Tuple[typing.List[str], Account]:
    """Encaches domain object: Account.
    
    :param account: Account domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "account",
        account.network,
        account.run_type,
        f"R-{str(account.run_index).zfill(3)}",
        str(account.index).zfill(6)
    ], account    


@cache_op(StorePartition.STATE, StoreOperation.SET)
def set_run_deploy(deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param deploy: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "deploy",
        deploy.network,
        deploy.run_type,
        f"R-{str(deploy.run_index).zfill(3)}",
        f"{str(deploy.dispatch_ts.timestamp())}.{deploy.deploy_hash}"
    ], deploy


@cache_op(StorePartition.STATE, StoreOperation.SET)
def set_run_transfer(transfer: Transfer) -> typing.Tuple[typing.List[str], Transfer]:
    """Encaches domain object: Transfer.
    
    :param transfer: Transfer domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "transfer",
        transfer.network,
        transfer.run_type,
        f"R-{str(transfer.run_index).zfill(3)}",
        transfer.asset.lower(),
        transfer.deploy_hash
    ], transfer
