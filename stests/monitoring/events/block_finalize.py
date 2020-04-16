from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.domain import NodeIdentifier
from stests.core.utils import logger


# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(node_id: NodeIdentifier, block_hash: str):   
    """Event: raised whenever a block is finalized.

    :param node_id: Identifier of node from which event was streamed.
    :param block_hash: Hash of finalized block.

    """
    logger.log(f"MONIT :: {node_id.label} -> block finalized :: {block_hash}")

    # TODO: use a block lock to handle concurrency rather than storing everything ?

    # Query: on-chain block info.
    block_info = clx.get_block_info(node_id, block_hash, parse=False)

    # Encache block info.
    cache.monitoring.set_block(factory.create_block_on_finalisation(
        node_id=node_id,
        block_hash=block_hash,
        deploy_cost_total=block_info.status.stats.deploy_cost_total,
        deploy_count=block_info.summary.header.deploy_count, 
        deploy_gas_price_avg=block_info.status.stats.deploy_gas_price_avg,
        j_rank=block_info.summary.header.j_rank,
        m_rank=block_info.summary.header.main_rank,
        size_bytes=block_info.status.stats.block_size_bytes,
        timestamp=datetime.fromtimestamp(block_info.summary.header.timestamp / 1000.0),
        validator_id=block_info.summary.header.validator_public_key.hex()
        )
    )
