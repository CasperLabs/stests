
from stests.chain import stream_events
from stests.core import cache
from stests.core.logging import log_event
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.events import EventType
from stests.monitoring import on_block_added
from stests.monitoring import on_block_finalized
from stests.monitoring import on_deploy_processed



# Map: event type -> callback.
CALLBACKS = {
    EventType.MONIT_BLOCK_ADD: on_block_added.callback,
    EventType.MONIT_BLOCK_FINALIZED: on_block_finalized.callback,
    EventType.MONIT_DEPLOY_PROCESSED: on_deploy_processed.callback,
}


def bind_to_stream(node: Node):
    """Binds to a node's event stream.

    :node: Node being monitored.
    
    """
    def _on_node_event(node: Node, info: NodeEventInfo, payload: dict):
        """Event callback.
        
        """
        # Escape if event already processed - happens if > 1 monitor per node.
        # NOTE: node software at present does not emit event identifiers.
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

        # Dispatch message to callback actor for further processing.
        CALLBACKS[info.event_type].send(node, info)

    # Bind to a node's stream-events endpoint & dispatch a message to relevant actor.
    stream_events(node, _on_node_event)
