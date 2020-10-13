from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(node_id: NodeIdentifier, info: NodeEventInfo):   
    """Event: raised whenever a block is finalized.

    :param node_id: Identifier of node from which event was streamed.
    :param info: Node event information.

    """
    print(_QUEUE)
    # # Escape if already processed.
    # if _already_processed(info):
    #     return

    # # Escape if on-chain block info not found.
    # block_info = clx.get_block_info(node_id, info.block_hash)
    # if block_info is None:
    #     log_event(EventType.CHAIN_QUERY_BLOCK_NOT_FOUND, None, node_id, block_hash=info.block_hash)
    #     return

    # # Escape if empty.
    # deploy_count=block_info['summary']['header'].get('deployCount', 0)    
    # if deploy_count == 0:
    #     return

    # # Emit event.
    # log_event(EventType.CHAIN_FINALIZED_BLOCK, f"{info.block_hash}", factory.create_block_statistics_on_finalization(
    #     block_hash=info.block_hash,
    #     chain_name=block_info['summary']['header']['chainName'],
    #     deploy_cost_total=block_info['status']['stats'].get('deployCostTotal'),
    #     deploy_count=deploy_count,
    #     deploy_gas_price_avg=block_info['status']['stats'].get('deployGasPriceAvg'),
    #     j_rank=block_info['summary']['header']['jRank'],
    #     m_rank=block_info['summary']['header']['mainRank'],
    #     magic_bit=block_info['summary']['header'].get('magicBit'),
    #     message_role=block_info['summary']['header']['messageRole'],
    #     network=node_id.network_name,
    #     round_id=block_info['summary']['header']['roundId'],
    #     size_bytes=block_info['status']['stats']['blockSizeBytes'],
    #     timestamp=datetime.fromtimestamp(block_info['summary']['header']['timestamp'] / 1000.0),
    #     validator_id=block_info['summary']['header']['validatorPublicKey'],        
    # ))


def _already_processed(info: NodeEventInfo) -> bool:
    """Returns flag indicating whether finalised deploy event has already been processed.

    """
    summary = factory.create_block_summary_on_finalisation(info)
    _, encached = cache.monitoring.set_block_summary(summary)

    return not encached
