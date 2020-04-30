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
    _import_actors()

    # Import dramatiq actor used to ping message to broker.
    from stests.workflows.orchestration.actors import do_run

    # Unpack args.
    network_id = factory.create_network_id(args.network_name)
    node_id = factory.create_node_id(network_id, args.node_index)

    # Start generator(s).    
    for ctx in _get_context_list(meta, args, network_id, node_id):
        do_run.send(ctx)
        logger.log(f"{ctx.run_type} :: run {ctx.run_index} started")


def _import_actors():
    """Import actors used during launch.
    
    """
    # Initialise broker.
    from stests.core import mq
    mq.initialise()

    # Initialise encoder.
    from stests.core.mq import encoder
    encoder.initialise()

    # Import actors: generators.
    import stests.workflows.generators.wg_100.meta
    import stests.workflows.generators.wg_110.meta
    import stests.workflows.generators.wg_200.meta
    import stests.workflows.generators.wg_210.meta


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
    # Set run identifier (unique to each run type).
    run_index = cache.orchestration.increment_generator_run_count(network_id.name, meta.TYPE)

    # Set run ctx.
    return factory.create_execution_context(
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
