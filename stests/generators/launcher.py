import argparse
import typing

from stests.core.utils import factory
from stests.core.utils import logger
from stests.orchestration.predicates import is_run_locked



def start_generator(meta):
    """Entry point.
    
    """
    # Parse cli args.        
    args = meta.ARGS.parse_args()

    # Import initialiser to setup upstream services / actors.
    import stests.initialiser

    # Unpack args.
    network_id = factory.create_network_id(args.network_name)
    node_id = factory.create_node_id(network_id, args.node_index)

    # Set execution context.
    ctx = factory.create_run_info(
        args=meta.Arguments.create(args),
        deploys_per_second=args.deploys_per_second,
        execution_mode=args.execution_mode,
        loop_count=args.loop_count,
        loop_interval=args.loop_interval,
        network_id=network_id,
        node_id=node_id,
        run_index=args.run_index,
        run_type=meta.TYPE
    )

    # Abort if a run lock cannot be acquired.
    if is_run_locked(ctx):
        logger.log_warning(f"{meta.TYPE} :: run {args.run_index} aborted as it is currently executing.")
        
    # Start run.
    else:
        from stests.orchestration.actors import do_run
        do_run.send(ctx)
        logger.log(f"{meta.TYPE} :: run {args.run_index} started")
