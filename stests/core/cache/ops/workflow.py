import typing

from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import SearchKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.utils import cache_op
from stests.core.types.orchestration import ExecutionContext



# Cache partition.
_PARTITION = StorePartition.WORKFLOW

# Cache collections.
COL_DEPLOY_COUNT = "deploy_count"


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_deploy_count(ctx: ExecutionContext, deploy_count: int) -> Item:
    """Encaches test deploy count.

    """
    return Item(
        data={
            'deploy_count': deploy_count,
        },
        item_key=ItemKey(
            paths=[
                ctx.network,
                ctx.run_type,
                ctx.label_run_index,
            ],
            names=[
                COL_DEPLOY_COUNT,
            ]
        )
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_deploy_count(ctx: ExecutionContext) -> ItemKey:
    """Decaches test deploy count.

    """
    return ItemKey(
        paths=[
            ctx.network,
            ctx.run_type,
            ctx.label_run_index,
        ],
        names=[
            COL_DEPLOY_COUNT,
        ],
    )
