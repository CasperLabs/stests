from stests import chain
from stests.core import cache
from stests.core.logging import log_event
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.events import EventType
from stests.monitoring.on_consensus_finality_signature import on_consensus_finality_signature



# Map: event type -> actor.
_ACTORS = {
    EventType.MONIT_CONSENSUS_FINALITY_SIGNATURE: on_consensus_finality_signature,
}


def bind_to_stream(node: Node, event_id: int = 0):
    """Binds to a node's event stream.

    :node: Node being monitored.
    :param event_id: Identifer of event from which to start stream.
    
    """
    chain.stream_events(node, _on_node_event)


def _on_node_event(node: Node, info: NodeEventInfo, payload: dict):
    """Event callback.
    
    """
    # Escape if event not of interest.
    if info.event_type not in _ACTORS:
        return

    # Escape if event already processed - happens when monitoring multiple nodes.
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
