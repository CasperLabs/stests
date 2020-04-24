import random
import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.ops_infra import get_network
from stests.core.cache.ops_infra import get_nodes
from stests.core.cache.utils import cache_op
from stests.core.types.chain import Account
from stests.core.types.chain import AccountIdentifier
from stests.core.types.chain import ContractType
from stests.core.types.chain import Deploy
from stests.core.types.chain import NamedKey
from stests.core.types.chain import Transfer
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core import factory



# Cache partition.
_PARTITION = StorePartition.STATE

# Cache collections.
COL_ACCOUNT = "account"
COL_ACCOUNT_BALANCE = "account-balance"
COL_NAMED_KEY = "named-key"
COL_DEPLOY = "deploy"
COL_TRANSFER = "transfer"


@cache_op(_PARTITION, StoreOperation.DECR)
def decrement_account_balance(account: Account, amount: int):
    """Updates (atomically) an account's (theoretical) balance.

    :param ctx: Execution context information.
    :param account: An account whose balance is being updated.
    :param amount: Balance delta to apply.

    """
    return [
        account.network,
        account.run_type,
        account.label_run_index,
        COL_ACCOUNT_BALANCE,
        account.label_index,
    ], amount
    

@cache_op(_PARTITION, StoreOperation.DECR)
def decrement_account_balance_on_deploy_finalisation(deploy: Deploy):
    """Updates (atomically) an account's (theoretical) balance.

    :param ctx: Execution context information.
    :param account: An account whose balance is being updated.
    :param amount: Balance delta to apply.

    """
    return [
        deploy.network,
        deploy.run_type,
        deploy.label_run_index,
        COL_ACCOUNT_BALANCE,
        deploy.label_account_index,
    ], deploy.cost * 10


@cache_op(_PARTITION, StoreOperation.GET)
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


@cache_op(_PARTITION, StoreOperation.GET_COUNT)
def get_account_balance(account: Account) -> int:
    """Returns balance of a test account.

    :param account: An account.

    :returns: Cached account balance.

    """
    return [
        account.network,
        account.run_type,
        account.label_run_index,
        COL_ACCOUNT_BALANCE,
        account.label_index,
    ]


def get_account_by_index(ctx: ExecutionContext, index: int) -> Account:
    """Decaches domain object: Account.
    
    :param ctx: Execution context information.
    :param index: Run specific account index. 

    :returns: A cached account.

    """
    return get_account(factory.create_account_id(
        index,
        ctx.network,
        ctx.run_index,
        ctx.run_type
        ))


@cache_op(_PARTITION, StoreOperation.GET_COUNT_MATCHED)
def get_account_count(ctx: ExecutionContext) -> int:
    """Returns count of accounts within the scope of an execution aspect.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    :returns: Count of accounts.

    """
    return [
        ctx.network,
        ctx.run_type,
        ctx.label_run_index,
        COL_ACCOUNT,
        "A-*"
    ]


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_deploy(deploy_hash: str) -> Deploy:
    """Decaches domain object: Deploy.
    
    :param deploy_hash: A deploy hash.

    :returns: A run deploy.

    """
    return [f"*{COL_DEPLOY}*{deploy_hash}*"]


@cache_op(_PARTITION, StoreOperation.GET)
def get_deploys(network_id: NetworkIdentifier, run_type: str, run_index: int = None) -> typing.List[Deploy]:
    """Decaches domain object: Deploy.
    
    :param ctx: Execution context information.
    :param run_type: Type of run that was executed.
    :param run_index: Index of a run.

    :returns: Keypath to domain object instance.

    """
    if not run_type:
        path = [
            network_id.name,
            "*",
            COL_DEPLOY,
            "*",
        ]
    elif run_index:
        label_run_index = f"R-{str(run_index).zfill(3)}"
        path = [
            network_id.name,
            run_type,
            label_run_index,
            COL_DEPLOY,
            "*",
        ]
    else:
        path = [
            network_id.name,
            run_type,
            "*",
            COL_DEPLOY,
            "*",
        ]

    return path


@cache_op(_PARTITION, StoreOperation.GET)
def get_deploys_by_account(ctx: ExecutionContext, account_index: int) -> typing.List[Deploy]:
    """Decaches domain object: Deploy.
    
    :param ctx: Execution context information.
    :param account_index: Index of an account.

    :returns: Keypath to domain object instance.

    """
    return [
        ctx.network,
        ctx.run_type,
        ctx.label_run_index,
        COL_DEPLOY,
        f"*.A-{str(account_index).zfill(6)}"
    ]


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_named_keys(ctx: ExecutionContext, account: Account, contract_type: ContractType) -> typing.List[NamedKey]:
    """Decaches domain objects: NamedKey.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    return [
        ctx.network,
        ctx.run_type,
        ctx.label_run_index,
        COL_NAMED_KEY,
        account.label_index,
        contract_type.name    
    ]


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_transfer(deploy_hash: str) -> Transfer:
    """Decaches domain object: Transfer.
    
    :param deploy_hash: A deploy hash.

    :returns: A run deploy.

    """
    return [
        "*",
        COL_TRANSFER,
        "*",
        deploy_hash,
    ]


@cache_op(_PARTITION, StoreOperation.INCR)
def increment_account_balance(account: Account, amount: int):
    """Updates (atomically) an account's (theoretical) balance.

    :param ctx: Execution context information.
    :param account: An account whose balance is being updated.
    :param amount: Balance delta to apply.

    """
    return [
        account.network,
        account.run_type,
        account.label_run_index,
        COL_ACCOUNT_BALANCE,
        account.label_index,
    ], amount


@cache_op(_PARTITION, StoreOperation.SET)
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


@cache_op(_PARTITION, StoreOperation.SET)
def set_deploy(deploy: Deploy) -> typing.Tuple[typing.List[str], Deploy]:
    """Encaches domain object: Deploy.
    
    :param deploy: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        deploy.network,
        deploy.run_type,
        deploy.label_run_index,
        COL_DEPLOY,
        f"{str(deploy.dispatch_ts.timestamp())}.{deploy.deploy_hash}.{deploy.label_account_index}"
    ], deploy


@cache_op(_PARTITION, StoreOperation.SET)
def set_named_key(ctx: ExecutionContext, named_key: NamedKey) -> typing.Tuple[typing.List[str], NamedKey]:
    """Encaches domain object: NamedKey.

    :param network: NamedKey domain object instance to be cached.
    
    :returns: Keypath + domain object instance.

    """
    return [
        named_key.network,
        named_key.run_type,
        named_key.label_run_index,
        COL_NAMED_KEY,
        named_key.label_account_index,
        named_key.contract_type.name,
        named_key.name,
    ], named_key


@cache_op(_PARTITION, StoreOperation.SET)
def set_transfer(transfer: Transfer) -> typing.Tuple[typing.List[str], Transfer]:
    """Encaches domain object: Transfer.
    
    :param transfer: Transfer domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        transfer.network,
        transfer.run_type,
        transfer.label_run_index,
        COL_TRANSFER,
        transfer.asset.lower(),
        transfer.deploy_hash
    ], transfer


def update_transfer(transfer: Transfer) -> typing.Tuple[typing.List[str], Transfer]:
    """Updates domain object: Transfer.
    
    :param transfer: Transfer domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return set_transfer(transfer)
