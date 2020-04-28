from stests.core import cache
from stests.core import clx
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventType
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
    NodeEventType.BLOCK_ADD: on_block_added,
    NodeEventType.BLOCK_FINALIZED: on_block_finalized,
    NodeEventType.DEPLOY_ADDED: on_deploy_added,
    NodeEventType.DEPLOY_DISCARDED: on_deploy_discarded,
    NodeEventType.DEPLOY_FINALIZED: on_deploy_finalized,
    NodeEventType.DEPLOY_ORPHANED: on_deploy_orphaned,
    NodeEventType.DEPLOY_PROCESSED: on_deploy_processed,
    NodeEventType.DEPLOY_REQUEUED: on_deploy_requeued,
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

        # Dispatch message to actor for further processing.
        logger.log(f"CHAIN :: {node.label_index} :: {event_info.event_type.name.ljust(17)} :: {event_info.log_suffix}")
        handler.send(node_id, event_info)

    # Bind to a node's stream-events endpoint & dispatch a message to relevant actor.
    clx.stream_events(node_id, _on_node_event)
