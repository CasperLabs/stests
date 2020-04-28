import random
import typing

from stests.core import factory
from stests.core.cache.model import CountDecrementKey
from stests.core.cache.model import CountIncrementKey
from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import SearchKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.infra import get_network
from stests.core.cache.ops.infra import get_nodes
from stests.core.cache.ops.utils import cache_op
from stests.core.types.chain import Account
from stests.core.types.chain import AccountIdentifier
from stests.core.types.chain import ContractType
from stests.core.types.chain import Deploy
from stests.core.types.chain import NamedKey
from stests.core.types.chain import Transfer
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import NodeEventInfo
from stests.core.types.orchestration import ExecutionContext



# Cache partition.
_PARTITION = StorePartition.STATE

# Cache collections.
COL_ACCOUNT = "account"
COL_ACCOUNT_BALANCE = "account-balance"
COL_NAMED_KEY = "named-key"
COL_DEPLOY = "deploy"
COL_TRANSFER = "transfer"


@cache_op(_PARTITION, StoreOperation.COUNTER_DECR)
def decrement_account_balance(account: Account, amount: int) -> CountDecrementKey:
    """Updates (atomically) an account's (theoretical) balance.

    :param account: An account whose balance is being updated.
    :param amount: Balance delta to apply.

    """
    return CountDecrementKey(
        paths=[
            account.network,
            account.run_type,
            account.label_run_index,
            COL_ACCOUNT_BALANCE,
        ],
        names=[
            account.label_index,
        ],
        amount=amount,
    )


@cache_op(_PARTITION, StoreOperation.COUNTER_DECR)
def decrement_account_balance_on_deploy_finalisation(deploy: Deploy) -> CountDecrementKey:
    """Updates (atomically) an account's (theoretical) balance.

    :param deploy: A finalised deploy.

    """
    return CountDecrementKey(
        paths=[
            deploy.network,
            deploy.run_type,
            deploy.label_run_index,
            COL_ACCOUNT_BALANCE,
        ],
        names=[
            deploy.label_account_index,
        ],
        amount=(deploy.cost * 10),
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_account(account_id: AccountIdentifier) -> ItemKey:
    """Decaches domain object: Account.

    :param account_id: An account identifier.

    :returns: A cached account.

    """
    return ItemKey(
        paths=[
            account_id.run.network.name,
            account_id.run.type,
            f"R-{str(account_id.run.index).zfill(3)}",
            COL_ACCOUNT,
        ],
        names=[
            account_id.label_index,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_COUNTER_ONE)
def get_account_balance(account: Account) -> ItemKey:
    """Returns balance of a test account.

    :param account: An account.

    :returns: Cached account balance.

    """
    return ItemKey(
        paths=[
            account.network,
            account.run_type,
            account.label_run_index,
            COL_ACCOUNT_BALANCE,
        ],
        names=[
            account.label_index,
        ],
    )


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


@cache_op(_PARTITION, StoreOperation.GET_COUNT)
def get_account_count(ctx: ExecutionContext) -> SearchKey:
    """Returns count of accounts within the scope of an execution aspect.

    :param ctx: Execution context information.
    :param aspect: Aspect of execution in scope.

    :returns: Count of accounts.

    """
    return SearchKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_ACCOUNT,
            "A-",
        ],
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE_FROM_MANY)
def get_deploy(ctx: ExecutionContext, deploy_hash: str) -> ItemKey:
    """Decaches domain object: Deploy.
    
    :param deploy_hash: A deploy hash.

    :returns: A run deploy.

    """
    return ItemKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_DEPLOY,
        ],
        names=[
            "*.*",
            deploy_hash,
            "A-*"
        ],
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE_FROM_MANY)
def get_deploy_by_node_event_info(info: NodeEventInfo) -> ItemKey:
    """Decaches domain object: Deploy.
    
    :param deploy_hash: A deploy hash.

    :returns: A run deploy.

    """
    return ItemKey(
        paths=[
            info.network,
            "WG-*",
            "R-*",
            COL_DEPLOY,
        ],
        names=[
            "*.*",
            info.deploy_hash,
            "A-*"
        ],
    )


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_deploys(network_id: NetworkIdentifier, run_type: str, run_index: int) -> SearchKey:
    """Decaches domain object: Deploy.
    
    :param ctx: Execution context information.
    :param run_type: Type of run that was executed.
    :param run_index: Index of a run.

    :returns: Keypath to domain object instance.

    """
    return SearchKey(
        paths=[
            network_id.name,
            run_type,
            f"R-{str(run_index).zfill(3)}",
            COL_DEPLOY,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_named_keys(ctx: ExecutionContext, account: Account, contract_type: ContractType) -> SearchKey:
    """Decaches domain objects: NamedKey.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    return SearchKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_NAMED_KEY,
            account.label_index,
            contract_type.name,            
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_transfer_by_deploy(deploy: Deploy, asset: str="CLX") -> ItemKey:
    """Decaches domain object: Transfer.
    
    :param deploy_hash: A deploy hash.

    :returns: A run deploy.

    """
    return ItemKey(
        paths=[
            deploy.network,
            deploy.run_type,
            deploy.label_run_index,
            COL_TRANSFER,
            asset.lower(),
        ],
        names=[
            deploy.hash,
        ],
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_transfer_by_ctx(ctx: ExecutionContext, deploy_hash: str, asset: str="CLX") -> ItemKey:
    """Decaches domain object: Transfer.
    
    :param deploy_hash: A deploy hash.

    :returns: A run deploy.

    """
    return ItemKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
            COL_TRANSFER,
            asset.lower(),
        ],
        names=[
            deploy_hash,
        ],
    )    


@cache_op(_PARTITION, StoreOperation.COUNTER_INCR)
def increment_account_balance(account: Account, amount: int) -> CountIncrementKey:
    """Updates (atomically) an account's (theoretical) balance.

    :param account: An account whose balance is being updated.
    :param amount: Balance delta to apply.

    """
    return CountIncrementKey(
        paths=[
            account.network,
            account.run_type,
            account.label_run_index,
            COL_ACCOUNT_BALANCE,
        ],
        names=[
            account.label_index,
        ],
        amount=amount,
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_account(account: Account) -> Item:
    """Encaches domain object: Account.
    
    :param account: Account domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return Item(
        data=account,
        item_key=ItemKey(
            paths=[
                account.network,
                account.run_type,
                f"R-{str(account.run_index).zfill(3)}",
                COL_ACCOUNT,
            ],
            names=[
                account.label_index,
            ]
        )
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_deploy(deploy: Deploy) -> Item:
    """Encaches domain object: Deploy.
    
    :param deploy: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return Item(
        data=deploy,
        item_key=ItemKey(
            paths=[
                deploy.network,
                deploy.run_type,
                deploy.label_run_index,
                COL_DEPLOY,
            ],
            names=[
                str(deploy.dispatch_ts.timestamp()),
                deploy.deploy_hash,
                deploy.label_account_index,
            ]
        )
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_named_key(ctx: ExecutionContext, named_key: NamedKey) -> Item:
    """Encaches domain object: NamedKey.

    :param network: NamedKey domain object instance to be cached.
    
    :returns: Keypath + domain object instance.

    """
    return Item(
        data=named_key,
        item_key=ItemKey(
            paths=[
                named_key.network,
                named_key.run_type,
                named_key.label_run_index,
                COL_NAMED_KEY,
                named_key.label_account_index,
                named_key.contract_type.name,
            ],
            names=[
                named_key.name,
            ]
        )
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_transfer(transfer: Transfer) -> Item:
    """Encaches domain object: Transfer.
    
    :param transfer: Transfer domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return Item(
        data=transfer,
        item_key=ItemKey(
            paths=[
                transfer.network,
                transfer.run_type,
                transfer.label_run_index,
                COL_TRANSFER,
                transfer.asset.lower(),
            ],
            names=[
                transfer.deploy_hash,
            ]
        )
    )
