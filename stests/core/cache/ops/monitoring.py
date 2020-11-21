from stests.core.cache.model import Item
from stests.core.cache.model import ItemKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.utils import cache_op
from stests.core.types.chain import BlockSummary
from stests.core.types.chain import DeploySummary
from stests.core.types.infra import NodeEventInfo


# Cache partition.
_PARTITION = StorePartition.MONITORING

# Cache collections.
COL_BLOCK_SUMMARY = "block-summary"
COL_DEPLOY_SUMMARY = "deploy-summary"
COL_EVENT = "event"



@cache_op(_PARTITION, StoreOperation.SET_ONE_SINGLETON)
def set_block_summary(summary: BlockSummary) -> Item:
    """Encaches an item.
    
    :param summary: Block summary instance to be cached.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                summary.network,
                COL_BLOCK_SUMMARY,
                summary.status.name,
            ],
            names=[
                summary.block_hash,
            ],
        ),
        data=summary
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE_SINGLETON)
def set_deploy_summary(summary: DeploySummary) -> Item:
    """Encaches an item.
    
    :param summary: Deploy summary instance to be cached.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                summary.network,
                COL_DEPLOY_SUMMARY,
            ],
            names=[
                summary.block_hash,
                summary.deploy_hash,
            ],
        ),
        data=summary
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE_SINGLETON)
def set_node_event_info(info: NodeEventInfo) -> Item:
    """Encaches an item.
    
    :param info: Node event information.

    :returns: Item to be cached.

    """
    return Item(
        item_key=ItemKey(
            paths=[
                info.network,
                COL_EVENT,
                info.label_node_index,
            ],
            names=[
                info.label_event_id,
                info.label_event_type,
            ],
        ),
        data=info
    )
