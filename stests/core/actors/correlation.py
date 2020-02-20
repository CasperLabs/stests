import dramatiq

from stests.core import cache
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus



# Queue to which messages will be dispatched.
_QUEUE = "correlators"


@dramatiq.actor(queue_name=_QUEUE)
def do_correlate_finalized_deploy(block_hash: str, deploy_hash: str, ts_finalized: int):   
    """Event: raised whenever a finalized deploy needs to be correlated back to a generator.
    
    :param block_hash: Hash of finalized block.
    :param deploy_hash: Hash of finalized deploy.
    :param ts_finalized: Moment in time when finalization occurred.

    """
    entities = cache.get_run_deploy_and_transfers(deploy_hash)
    if not entities:
        return

    for entity in entities:
        if isinstance(entity, Deploy):
            entity.block_hash = block_hash
            entity.status = DeployStatus.FINALIZED
            entity.ts_finalized = ts_finalized
            cache.set_run_deploy(entity)

        if isinstance(entity, Transfer):
            entity.status = TransferStatus.COMPLETE
            cache.set_run_transfer(entity)
