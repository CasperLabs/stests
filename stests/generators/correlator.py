import dramatiq

from stests.generators.wg_100.orchestrator import on_deploy_finalized as wg_100


# Queue to which messages will be dispatched.
_QUEUE = "generators"


# Map of workload generator run type to finalized deploy handlers.
CORRELATION_HANDLERS = {
    "WG-100": wg_100,
}


@dramatiq.actor(queue_name=_QUEUE)
def correlate_finalized_deploy(run_type: str, deploy_hash: str):   
    """Correlates a finalzied deploy with a workload generator correlation handler.
    
    :param run_type: Type of generator run.
    :param deploy_hash: Hash of finalized deploy.

    """
    if run_type in CORRELATION_HANDLERS:
        CORRELATION_HANDLERS[run_type].send(deploy_hash)
