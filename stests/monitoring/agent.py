from stests.core import cache
from stests.core import clx
from stests.core.utils import logger
from stests.core.domain import NodeIdentifier
from stests.monitoring import events



def monitor_node(node_id: NodeIdentifier):
    """Monitors a particular node.

    :node_id: Identifier of node being monitored.
    
    """
    logger.log(f"MTRNG :: node :: start :: {node_id.label}")

    def _on_block_added(_, event_id, block_hash):
        events.on_block_added.send(node_id, block_hash)

    def _on_block_finalized(_, event_id, block_hash):
        events.on_block_finalized.send(node_id, block_hash)

    def _on_deploy_added(_, event_id, deploy_hash):
        events.on_deploy_added.send(node_id, deploy_hash)

    def _on_deploy_discarded(_, event_id, deploy_hash):
        events.on_deploy_discarded.send(node_id, deploy_hash)

    def _on_deploy_finalized(_, event_id, block_hash, deploy_hash):
        events.on_deploy_finalized.send(node_id, block_hash, deploy_hash)

    def _on_deploy_orphaned(_, event_id, deploy_hash):
        events.on_deploy_orphaned.send(node_id, deploy_hash)

    def _on_deploy_processed(_, event_id, block_hash, deploy_hash):
        events.on_deploy_processed.send(node_id, block_hash, deploy_hash)

    def _on_deploy_requeued(_, event_id, block_hash, deploy_hash):
        events.on_deploy_requeued.send(node_id, block_hash, deploy_hash)

    # Bind to stream & route events to message dispatchers.
    clx.stream_events(node_id,
        # Block events.
        on_block_added=_on_block_added,
        on_block_finalized=_on_block_finalized,
        # Deploy events.
        on_deploy_added=_on_deploy_added,
        on_deploy_discarded=_on_deploy_discarded,
        on_deploy_finalized=_on_deploy_finalized,
        on_deploy_orphaned=_on_deploy_orphaned,
        on_deploy_processed=_on_deploy_processed,
        on_deploy_requeued=_on_deploy_requeued,
        )
