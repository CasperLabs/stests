import argparse
import typing

from stests.core.utils import factory
from stests.core.utils import logger
from stests.core.orchestration import ExecutionContext
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

    # Start generators in parallel.    
    for ctx in _get_ctx_list(meta, args, network_id, node_id):
        _start(ctx)


def _get_ctx_list(meta, args, network_id, node_id) -> typing.Generator:
    return map(
        lambda i: _get_ctx(meta, args, network_id, node_id, i), 
        range(1, args.parallel_count + 1)
        )


def _get_ctx(meta, args, network_id, node_id, run_offset) -> ExecutionContext:
    """Returns run specific execution context.
    
    """
    return factory.create_run_info(
        args=meta.Arguments.create(args),
        deploys_per_second=args.deploys_per_second,
        execution_mode=args.execution_mode,
        loop_count=args.loop_count,
        loop_interval=args.loop_interval,
        network_id=network_id,
        node_id=node_id,
        run_index=args.run_index + run_offset -1,
        run_type=meta.TYPE
    )


def _start(ctx: ExecutionContext):
    """Attempt to start a generator.
    
    """
    # JIT import to avoid import collision.
    from stests.orchestration.actors import do_run

    # Abort if a run lock cannot be acquired.
    if is_run_locked(ctx):
        logger.log_warning(f"{ctx.run_type} :: run {ctx.run_index} aborted as it is currently executing.")
        return
        
    # Start run.
    do_run.send(ctx)
    logger.log(f"{ctx.run_type} :: run {ctx.run_index} started")
