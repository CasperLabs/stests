
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
    def _on_node_event(node: Node, event_info: NodeEventInfo):
        """Event callback.
        
        """
        # Set handler.
        handler = HANDLERS[event_info.event_type]

        # Escape if event already processed - happens if > 1 monitor per node.
        if event_info.event_id:
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
    stream_events(node, lambda node, event_info: print(event_info))
