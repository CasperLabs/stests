from stests.core import cache
from stests.core import clx
from stests.core.logging import log_event
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.monitoring.callbacks.block_add import on_block_added
from stests.monitoring.callbacks.block_finalize import on_block_finalized
from stests.monitoring.callbacks.deploy_add import on_deploy_added
from stests.monitoring.callbacks.deploy_discard import on_deploy_discarded
from stests.monitoring.callbacks.deploy_finalize import on_deploy_finalized
from stests.monitoring.callbacks.deploy_orphan import on_deploy_orphaned
from stests.monitoring.callbacks.deploy_processed import on_deploy_processed
from stests.monitoring.callbacks.deploy_requeue import on_deploy_requeued
from stests.events import EventType



# Map: event type -> handler.
HANDLERS = {
    EventType.MONIT_BLOCK_ADD: on_block_added,
    EventType.MONIT_BLOCK_FINALIZED: on_block_finalized,
    EventType.MONIT_DEPLOY_ADDED: on_deploy_added,
    EventType.MONIT_DEPLOY_DISCARDED: on_deploy_discarded,
    EventType.MONIT_DEPLOY_FINALIZED: on_deploy_finalized,
    EventType.MONIT_DEPLOY_ORPHANED: on_deploy_orphaned,
    EventType.MONIT_DEPLOY_PROCESSED: on_deploy_processed,
    EventType.MONIT_DEPLOY_REQUEUED: on_deploy_requeued,
}


def bind_to_stream(node_id: NodeIdentifier):
    """Binds to a node's event stream.

    :node_id: Identifier of node being monitored.
    
    """
    def _on_node_event(node: Node, event_info: NodeEventInfo):
        """Event callback.
        
        """
        # Escape if no handler.
        try:
            handler = HANDLERS[event_info.event_type]
        except KeyError:
            return

        # Escape if node event already processed - happens if > 1 monitor per node.
        _, was_lock_acquired = cache.monitoring.set_node_event_info(event_info)
        if not was_lock_acquired:
            return

        # Notify.
        log_event(
            event_info.event_type,
            None,
            node,
            event_id=event_info.event_id,
            block_hash=event_info.block_hash,
            deploy_hash=event_info.deploy_hash
            )

        # Dispatch message to actor for further processing.
        handler.send(node_id, event_info)

    # Bind to a node's stream-events endpoint & dispatch a message to relevant actor.
    clx.stream_events(node_id, _on_node_event)
