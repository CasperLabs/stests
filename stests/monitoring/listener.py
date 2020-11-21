
from stests.chain import stream_events
from stests.core import cache
from stests.core.logging import log_event
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.events import EventType
from stests.monitoring.on_block_added import on_block_added
from stests.monitoring.on_block_finalized import on_block_finalized
from stests.monitoring.on_deploy_processed import on_deploy_processed



# Map: event type -> actor.
_ACTORS = {
    EventType.MONIT_BLOCK_ADDED: on_block_added,
    EventType.MONIT_BLOCK_FINALIZED: on_block_finalized,
    EventType.MONIT_DEPLOY_PROCESSED: on_deploy_processed,
}


def bind_to_stream(node: Node, event_id: int = 0):
    """Binds to a node's event stream.

    :node: Node being monitored.
    :param event_id: Identifer of event from which to start stream.
    
    """
    # Bind to a node's events endpoint & invoke callback upon event receipt.
    stream_events(node, _on_node_event)


def _on_node_event(node: Node, info: NodeEventInfo, payload: dict):
    """Event callback.
    
    """
    # Escape if event already processed - happens if > 1 monitor per node.
    # NOTE: node software at present does not emit event identifiers
    #       therefore this logic gate will never be opened.
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
    actor = _ACTORS[info.event_type]
    actor.send(info)
