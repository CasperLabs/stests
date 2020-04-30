from stests.core import cache
from stests.core import clx
from stests.core.logging import log_event
from stests.core.logging import MonitoringEventType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.core.utils import logger
from stests.monitoring.events.block_add import on_block_added
from stests.monitoring.events.block_finalize import on_block_finalized
from stests.monitoring.events.deploy_add import on_deploy_added
from stests.monitoring.events.deploy_discard import on_deploy_discarded
from stests.monitoring.events.deploy_finalize import on_deploy_finalized
from stests.monitoring.events.deploy_orphan import on_deploy_orphaned
from stests.monitoring.events.deploy_processed import on_deploy_processed
from stests.monitoring.events.deploy_requeue import on_deploy_requeued



# Map: event type -> handler.
HANDLERS = {
    MonitoringEventType.BLOCK_ADD: on_block_added,
    MonitoringEventType.BLOCK_FINALIZED: on_block_finalized,
    MonitoringEventType.DEPLOY_ADDED: on_deploy_added,
    MonitoringEventType.DEPLOY_DISCARDED: on_deploy_discarded,
    MonitoringEventType.DEPLOY_FINALIZED: on_deploy_finalized,
    MonitoringEventType.DEPLOY_ORPHANED: on_deploy_orphaned,
    MonitoringEventType.DEPLOY_PROCESSED: on_deploy_processed,
    MonitoringEventType.DEPLOY_REQUEUED: on_deploy_requeued,
}


def bind_to_stream(node_id: NodeIdentifier):
    """Binds to a node's event stream.

    :node_id: Identifier of node being monitored.
    
    """
    def _on_node_event(node: Node, event_info: NodeEventInfo):
        # Escape if no handler.
        try:
            handler = HANDLERS[event_info.event_type]
        except KeyError:
            return
        
        # Escape if event already processed.
        _, was_lock_acquired = cache.monitoring.set_node_event_info(event_info)
        if not was_lock_acquired:
            return

        # Inform.
        log_event(event_info.event_type, node_id, event_id=event_info.event_id, block_hash=event_info.block_hash, deploy_hash=event_info.deploy_hash)

        # Dispatch message to actor for further processing.
        handler.send(node_id, event_info)

    # Bind to a node's stream-events endpoint & dispatch a message to relevant actor.
    clx.stream_events(node_id, _on_node_event)
