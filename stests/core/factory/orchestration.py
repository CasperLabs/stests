import os
import pwd
import typing
import uuid
from datetime import datetime

from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.orchestration import ExecutionContext
from stests.core.types.orchestration import ExecutionIdentifier
from stests.core.types.orchestration import ExecutionInfo
from stests.core.types.orchestration import ExecutionLock
from stests.core.types.orchestration import ExecutionMode
from stests.core.types.orchestration import ExecutionStatus



def create_execution_context(
    args: typing.Any,
    prune_on_completion: bool,
    deploys_per_second: int,
    key_algorithm: str,
    loop_count: int,
    loop_interval_ms: int,
    execution_mode: str,
    network_id: NetworkIdentifier,
    node_id: NodeIdentifier,
    run_index: int,
    run_type: str
    ) -> ExecutionContext:
    """Returns an orchestration object instance: ExecutionContext.
    
    """
    return ExecutionContext(
        args=args,
        prune_on_completion=prune_on_completion,
        deploys_per_second=deploys_per_second,
        execution_mode=ExecutionMode[execution_mode.upper()],
        key_algorithm=key_algorithm,
        loop_count=loop_count,
        loop_index=0,
        loop_interval_ms=loop_interval_ms,
        network=network_id.name,
        node_index=node_id.index,
        run_index=run_index,
        run_index_parent=None,
        run_type=run_type,
        phase_index=0,
        status=ExecutionStatus.IN_PROGRESS,
        step_index=0,
        step_label=None,
        uid=str(uuid.uuid4()),
    )
    

def create_execution_id(network_id: NetworkIdentifier, run_index: int, run_type: str) -> ExecutionIdentifier:
    """Returns a cache identifier: ExecutionIdentifier.
    
    """
    return ExecutionIdentifier(network_id, run_index, run_type)


def create_execution_info(aspect: ExecutionAspect, ctx: ExecutionContext) -> ExecutionInfo:
    """Returns an orchestration object instance: ExecutionInfo.
    
    """
    info = ExecutionInfo(
        aspect=aspect,
        network=ctx.network,
        phase_index=None,
        run_index=ctx.run_index,
        run_index_parent=ctx.run_index_parent,
        run_type=ctx.run_type,
        status=ExecutionStatus.IN_PROGRESS,
        step_index=None,
        step_label=None,
        tp_duration=None,
        ts_start=datetime.utcnow(),
        ts_end=None,
    )

    if aspect == ExecutionAspect.PHASE:
        info.phase_index = ctx.phase_index
    elif aspect == ExecutionAspect.STEP:
        info.phase_index = ctx.phase_index
        info.step_index = ctx.step_index
        info.step_label = ctx.step_label

    return info


def create_execution_lock(
    aspect: ExecutionAspect,
    network: str,
    run_index: int,
    run_type: str,
    phase_index: int,
    step_index: int,
    ) -> ExecutionLock:
    """Returns an orchestration object instance: ExecutionLock.
    
    """
    return ExecutionLock(
        aspect=aspect,
        network=network,
        run_index=run_index,
        run_type=run_type,
        phase_index=phase_index,
        step_index=step_index,
    )
