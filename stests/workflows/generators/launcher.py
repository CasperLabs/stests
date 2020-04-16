import argparse
import typing

from stests.core import cache
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import NodeIdentifier
from stests.core import factory
from stests.core.utils import logger
from stests.core.types.orchestration import ExecutionContext



def start_generator(meta: typing.Any):
    """Entry point.

    :param meta: Generator meta-data.

    """
    # Parse cli args.        
    args = meta.ARGS.parse_args()

    # Import worker to setup upstream services / actors.
    import stests.workflows.worker

    # Import dramatiq actor used to ping message to broker.
    from stests.workflows.orchestration.actors import do_run

    # Unpack args.
    network_id = factory.create_network_id(args.network_name)
    node_id = factory.create_node_id(network_id, args.node_index)

    # Start generator(s).    
    for ctx in _get_context_list(meta, args, network_id, node_id):
        do_run.send(ctx)
        logger.log(f"{ctx.run_type} :: run {ctx.run_index} started")


def _get_context_list(
    meta: typing.Any,
    args: argparse.Namespace,
    network_id: NetworkIdentifier,
    node_id: NodeIdentifier
    ) -> typing.Generator:
    """Returns collection of contextual information passed along chain of execution.
    
    """
    return map(
        lambda _: _get_context(meta, args, network_id, node_id), 
        range(1, args.parallel_count + 1)
        )


def _get_context(
    meta: typing.Any,
    args: argparse.Namespace,
    network_id: NetworkIdentifier,
    node_id: NodeIdentifier
    ) -> ExecutionContext:
    """Returns contextual information passed along chain of execution.
    
    """
    # Set unique run identifier.
    run_index = cache.orchestration.increment_generator_run_count(network_id.name, meta.TYPE)

    # Set run ctx.
    ctx = factory.create_execution_context(
        args=meta.Arguments.create(args),
        deploys_per_second=args.deploys_per_second,
        execution_mode=args.execution_mode,
        loop_count=args.loop_count,
        loop_interval=args.loop_interval,
        network_id=network_id,
        node_id=node_id,
        run_index=run_index,
        run_type=meta.TYPE
    )

    # Allow generator to mutate ctx.
    try:
        meta.parse_ctx
    except AttributeError:
        pass
    else:
        meta.parse_ctx(ctx)

    return ctx