from stests.core import clx
from stests.core.domain import NodeIdentifier
from stests.core.utils import logger
from stests.monitoring.events.block_add import on_block_added
from stests.monitoring.events.block_finalize import on_block_finalized
from stests.monitoring.events.deploy_add import on_deploy_added
from stests.monitoring.events.deploy_discard import on_deploy_discarded
from stests.monitoring.events.deploy_finalize import on_deploy_finalized
from stests.monitoring.events.deploy_orphan import on_deploy_orphaned
from stests.monitoring.events.deploy_processed import on_deploy_processed
from stests.monitoring.events.deploy_requeue import on_deploy_requeued



def bind_to_stream(node_id: NodeIdentifier):
    """Binds to a node's event stream.

    :node_id: Identifier of node being monitored.
    
    """
    logger.log(f"MTRNG :: node :: start :: {node_id.label}")

    def _on_block_added(_, event_id, block_hash):
        on_block_added.send(node_id, block_hash)

    def _on_block_finalized(_, event_id, block_hash):
        on_block_finalized.send(node_id, block_hash)

    def _on_deploy_added(_, event_id, deploy_hash):
        on_deploy_added.send(node_id, deploy_hash)

    def _on_deploy_discarded(_, event_id, deploy_hash):
        on_deploy_discarded.send(node_id, deploy_hash)

    def _on_deploy_finalized(_, event_id, block_hash, deploy_hash):
        on_deploy_finalized.send(node_id, block_hash, deploy_hash)

    def _on_deploy_orphaned(_, event_id, deploy_hash):
        on_deploy_orphaned.send(node_id, deploy_hash)

    def _on_deploy_processed(_, event_id, block_hash, deploy_hash):
        on_deploy_processed.send(node_id, block_hash, deploy_hash)

    def _on_deploy_requeued(_, event_id, block_hash, deploy_hash):
        on_deploy_requeued.send(node_id, block_hash, deploy_hash)

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