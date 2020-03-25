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



# Cache collections.
COL_ACCOUNT = "account"
COL_ACCOUNT_CONTRACT = "account-contract"
COL_DEPLOY = "deploy"
COL_TRANSFER = "transfer"


@cache_op(StorePartition.STATE, StoreOperation.FLUSH)
def flush_by_run(ctx: ExecutionContext) -> typing.Generator:
    """Flushes previous run information.

    :param ctx: Execution context information.

    :returns: A generator of keypaths to be flushed.
    
    """
    for collection in [
        COL_ACCOUNT,
        COL_ACCOUNT_CONTRACT,
        COL_DEPLOY,
        COL_TRANSFER,
    ]:
        yield [
            ctx.network,
            ctx.run_type,
            ctx.run_index_label,
            collection,
            "*"
        ]


@cache_op(StorePartition.STATE, StoreOperation.GET)
def get_account(account_id: AccountIdentifier) -> Account:
    """Decaches domain object: Account.

    :param account_id: An account identifier.

    :returns: A cached account.

    """
    return [
        account_id.run.network.name,
        account_id.run.type,
        f"R-{str(account_id.run.index).zfill(3)}",
        COL_ACCOUNT,
        account_id.label_index
    ]


def get_account_by_index(ctx: ExecutionContext, index: int) -> Account:
    """Decaches domain object: Account.
    
    :param ctx: Execution context information.
    :param index: Run specific account index. 

    :returns: A cached account.

    """
    account_id = factory.create_account_id(
        index,
        ctx.network,
        ctx.run_index,
        ctx.run_type
        )

    return get_account(account_id)


@cache_op(StorePartition.STATE, StoreOperation.GET_ONE)
def get_deploy(dhash: str) -> Deploy:
    """Decaches domain object: Deploy.
    
    :param dhash: A deploy hash.

    :returns: A run deploy.

    """    
    return [f"*{COL_DEPLOY}*{dhash}*"]


@cache_op(StorePartition.STATE, StoreOperation.GET)
def get_deploys(network_id: NetworkIdentifier, run_type: str, run_index: int = None) -> typing.List[Deploy]:
    """Decaches domain object: Deploy.
    
    :param ctx: Execution context information.
    :param run_type: Type of run that was executed.
    :param run_index: Index of a run.

    :returns: Keypath to domain object instance.

    """
    if not run_type:
        return [
            network_id.name,
            "*",
            COL_DEPLOY,
            "*",
        ]
    elif run_index:
        run_index_label = f"R-{str(run_index).zfill(3)}"
        return [
            network_id.name,
            run_type,
            run_index_label,
            COL_DEPLOY,
            "*",
        ]
    else:
        return [
            network_id.name,
            run_type,
            "*",
            COL_DEPLOY,
            "*",
        ]


@cache_op(StorePartition.STATE, StoreOperation.GET)
def get_deploys_by_account(ctx: ExecutionContext, account_index: int) -> typing.List[Deploy]:
    """Decaches domain object: Deploy.
    
    :param ctx: Execution context information.
    :param account_index: Index of an account.

    :returns: Keypath to domain object instance.

    """
    return [
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        COL_DEPLOY,
        f"*.A-{str(account_index).zfill(6)}"
    ]


def get_transfer(dhash: str) -> Transfer:
    """Decaches domain object: Transfer.
    
    :param dhash: A deploy hash.

    :returns: A run deploy.

    """    
    transfers = get_transfers(dhash)

    return transfers[-1] if transfers else None


@cache_op(StorePartition.STATE, StoreOperation.GET)
def get_transfers(dhash: str) -> typing.List[Transfer]:
    """Decaches collection of domain objects: Transfer.
    
    :param dhash: A deploy hash.

    :returns: Matched transfers.

    """    
    return [f"*{COL_TRANSFER}*{dhash}*"]


@cache_op(StorePartition.STATE, StoreOperation.SET)
def set_account(account: Account) -> typing.Tuple[typing.List[str], Account]:
    """Encaches domain object: Account.
    
    :param account: Account domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        account.network,
        account.run_type,
        f"R-{str(account.run_index).zfill(3)}",
        COL_ACCOUNT,
        account.label_index,
    ], account    


@cache_op(StorePartition.STATE, StoreOperation.SET)
def set_contract(contract: Contract) -> typing.Tuple[typing.List[str], Contract]:
    """Encaches domain object: Contract.
    
    :param contract: Contract domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    path = [
        contract.network,
        contract.run_type,
        contract.label_run_index,
        COL_ACCOUNT_CONTRACT,
        f"{contract.label_account_index}.{contract.typeof.name}",
    ]

    return path, contract


@cache_op(StorePartition.STATE, StoreOperation.SET)
def set_deploy(deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param deploy: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        deploy.network,
        deploy.run_type,
        f"R-{str(deploy.run_index).zfill(3)}",
        COL_DEPLOY,
        f"{str(deploy.dispatch_ts.timestamp())}.{deploy.deploy_hash}.{deploy.label_account_index}"
    ], deploy


@cache_op(StorePartition.STATE, StoreOperation.SET)
def set_transfer(transfer: Transfer) -> typing.Tuple[typing.List[str], Transfer]:
    """Encaches domain object: Transfer.
    
    :param transfer: Transfer domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        transfer.network,
        transfer.run_type,
        f"R-{str(transfer.run_index).zfill(3)}",
        COL_TRANSFER,
        transfer.asset.lower(),
        transfer.deploy_hash
    ], transfer
