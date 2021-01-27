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

    :returns: Cache decrement key.

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
def decrement_account_balance_on_deploy_finalisation(deploy: Deploy, cost: int) -> CountDecrementKey:
    """Updates (atomically) an account's (theoretical) balance.

    :returns: Cache decrement key.

    """
    # Escape if processing a deploy dispatched under network faucet.
    if deploy.is_from_network_faucet:
        return
    
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
        amount=(cost * 10),
    )


@cache_op(_PARTITION, StoreOperation.DELETE_MANY)
def prune_on_run_completion(ctx: ExecutionContext) -> SearchKey:
    """Deletes data cached during the course of a run.

    :param ctx: Execution context information.
    :returns: Cache search key under which all records will be deleted.

    """
    return SearchKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_account(account_id: AccountIdentifier) -> ItemKey:
    """Decaches domain object: Account.
    :param account_id: An account identifier.
    :returns: Cache item key.
    """
    return ItemKey(
        paths=[
            account_id.run.network.name,
            account_id.run.type,
            account_id.label_run_index,
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
    :returns: Cache item key.
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


@cache_op(_PARTITION, StoreOperation.GET_ONE_FROM_MANY)
def get_deploy(ctx: ExecutionContext, deploy_hash: str) -> ItemKey:
    """Decaches domain object: Deploy.

    :param ctx: Execution context information.    
    :param deploy_hash: A deploy hash.

    :returns: Cache item key.

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
def get_deploy_on_finalisation(network_name: str, deploy_hash: str) -> ItemKey:
    """Decaches domain object: Deploy.
    
    :param network_name: Name of network to which deploy was dispatched.
    :param deploy_hash: A deploy hash.

    :returns: Cache item key.

    """
    return ItemKey(
        paths=[
            network_name,
            "WG-*",
            "R-*",
            COL_DEPLOY,
        ],
        names=[
            "*.*",
            deploy_hash,
            "A-*"
        ],
    )


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_deploys(network_id: NetworkIdentifier, run_type: str, run_index: int) -> SearchKey:
    """Decaches domain object: Deploy.
    
    :param ctx: Execution context information.
    :param run_type: Type of run that was executed.
    :param run_index: Index of a run.

    :returns: Cache search key.

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

    :returns: Cache search key.

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


@cache_op(_PARTITION, StoreOperation.COUNTER_INCR)
def increment_account_balance(account: Account, amount: int) -> CountIncrementKey:
    """Updates (atomically) an account's (theoretical) balance.

    :param account: An account whose balance is being updated.
    :param amount: Balance delta to apply.

    :returns: Cache increment key.

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
    :returns: Cache item.
    """
    return Item(
        data=account,
        item_key=ItemKey(
            paths=[
                account.network,
                account.run_type,
                account.label_run_index,
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

    :returns: Cache item.

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
                str(deploy.dispatch_timestamp.timestamp()),
                deploy.deploy_hash,
                deploy.label_account_index,
            ]
        )
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_named_key(ctx: ExecutionContext, named_key: NamedKey) -> Item:
    """Encaches domain object: NamedKey.

    :param network: NamedKey domain object instance to be cached.
    
    :returns: Cache item.

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
