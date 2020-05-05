from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(node_id: NodeIdentifier, event_info: NodeEventInfo):   
    """Event: raised whenever a block is finalized.

    :param node_id: Identifier of node from which event was streamed.
    :param event_info: Node event information.

    """
    block_hash = event_info.block_hash

    # Query: on-chain block info.
    block_info = clx.get_block_info(node_id, block_hash)
    if block_info is None:
        log_event(EventType.MONITORING_BLOCK_NOT_FOUND, None, node_id, block_hash=block_hash)

    # Set stats.
    stats = factory.create_block_statistics_on_finalization(
        block_hash=event_info.block_hash,
        chain_name=block_info['summary']['header']['chainName'],
        deploy_cost_total=block_info['status']['stats']['deployCostTotal'],
        deploy_count=block_info['summary']['header']['deployCount'],
        deploy_gas_price_avg=block_info['status']['stats']['deployGasPriceAvg'],
        j_rank=block_info['summary']['header']['jRank'],
        m_rank=block_info['summary']['header']['mainRank'],
        network=node_id.network_name,
        node_index=node_id.index,
        size_bytes=block_info['status']['stats']['blockSizeBytes'],
        timestamp=datetime.fromtimestamp(block_info['summary']['header']['timestamp'] / 1000.0),
        validator_id=block_info['summary']['header']['validatorPublicKey'],        
    )

    # Emit event.
    log_event(EventType.CHAININFO_BLOCK_STATS, None, stats)
