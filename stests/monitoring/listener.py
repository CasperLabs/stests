
from stests.chain import stream_events
from stests.core import cache
from stests.core.logging import log_event
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.events import EventType
from stests.monitoring.callbacks import on_block_added
from stests.monitoring.callbacks import on_block_finalized
from stests.monitoring.callbacks import on_deploy_processed



# Map: event type -> handler.
HANDLERS = {
    EventType.MONIT_BLOCK_ADD: on_block_added,
    EventType.MONIT_BLOCK_FINALIZED: on_block_finalized,
    EventType.MONIT_DEPLOY_PROCESSED: on_deploy_processed,
}


def bind_to_stream(node: Node):
    """Binds to a node's event stream.

    :node: Node being monitored.
    
    """
    def _on_node_event(node: Node, info: NodeEventInfo, payload: dict):
        """Event callback.
        
        """
        # Set handler.
        handler = HANDLERS[info.event_type]

        # Escape if event already processed - happens if > 1 monitor per node.
        if info.event_id:
            _, was_lock_acquired = cache.monitoring.set_node_event_info(info)
            if not was_lock_acquired:
                return

        # Notify.
        log_event(
            info.event_type,
            None,
            node,
            event_id=info.event_id,
            block_hash=info.block_hash,
            deploy_hash=info.deploy_hash
            )

        # Dispatch message to actor for further processing.
        handler.send(node, info)

    # Bind to a node's stream-events endpoint & dispatch a message to relevant actor.
    stream_events(node, _on_node_event)
