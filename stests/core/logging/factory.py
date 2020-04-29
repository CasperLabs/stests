import datetime
import os
import platform
import pwd
import socket
import typing
import uuid

from stests.core.logging.types import ContextualLogInfo
from stests.core.logging.types import MonitoringLogInfo
from stests.core.logging.types import WorkflowLogInfo
from stests.core.logging.types import Level
from stests.core.logging.types import SubSystem
from stests.core.types.infra import NodeEventType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core.types.orchestration import ExecutionEventType



def get_monitoring_event_info(
    event_type: NodeEventType,
    node: typing.Union[Node, NodeIdentifier],
    message: str = None,
    event_id: str = None,
    block_hash: str = None,
    deploy_hash: str = None,
    ) -> MonitoringLogInfo:
    """Returns monitoring related log event information.
    
    """
    event_id=event_id or event_type.value
    is_error = event_type in (
        NodeEventType.DEPLOY_DISCARDED,
        NodeEventType.DEPLOY_ORPHANED,
        NodeEventType.API_ERROR,
        )
    is_warning = event_type in (
        NodeEventType.BLOCK_NOT_FOUND,
        NodeEventType.DEPLOY_REQUEUED,
        )
    message=f"{event_type.name} :: {str(message)}" if message else event_type.name
    level = Level.ERROR if is_error else Level.WARN if is_warning else Level.INFO
    priority=9 if is_error else 7 if is_warning else 5

    return MonitoringLogInfo(
        message=message,
        network=node.network_name,
        node_index=node.label_index,
        block_hash=block_hash,
        deploy_hash=deploy_hash,
        context=_get_context_info(
            event_id=event_id,
            event_type=event_type.name,
            level=level,
            priority=priority,
            sub_system=SubSystem.MONITORING,
        )
    )


def get_workflow_event_info(
    event_type: ExecutionEventType,
    ctx: ExecutionContext,
    message: typing.Union[BaseException, str] = None,
    ) -> WorkflowLogInfo:
    """Returns workflow related log event information.
    
    """
    event_id=event_type.value
    is_error = event_type in (
        ExecutionEventType.RUN_ERROR,
        ExecutionEventType.PHASE_ERROR,
        ExecutionEventType.STEP_ERROR,
        )
    is_warning = event_type in (
        ExecutionEventType.RUN_ABORT,
        ExecutionEventType.PHASE_ABORT,
        ExecutionEventType.STEP_ABORT,
        ExecutionEventType.STEP_FAILURE,
        )
    message=f"{event_type.name} :: {str(message)}" if message else event_type.name
    level = Level.ERROR if is_error else Level.WARN if is_warning else Level.INFO
    priority=9 if is_error else 7 if is_warning else 5

    return WorkflowLogInfo(
        message=message,
        network=ctx.network,
        phase_index=ctx.phase_index,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        step_index=ctx.step_index,
        step_label=ctx.step_label,        
        context=_get_context_info(
            event_id=event_id,
            event_type=event_type.name,
            level=level,
            priority=priority,
            sub_system=SubSystem.WORKFLOW,
        )
    )


def _get_context_info(
    event_id: int,
    event_type: str,
    level: Level,
    priority: int,
    sub_system: SubSystem,
    ) -> ContextualLogInfo:
    """Returns log event metadata.
    
    """
    return ContextualLogInfo(
        event_id=event_id,
        event_type=event_type,
        event_uid=str(uuid.uuid4()),
        host_name=socket.gethostname(),
        level=level.name,
        net_name=platform.node(),
        os_user=pwd.getpwuid(os.getuid())[0],
        priority=priority,
        process_id=str(os.getpid()).zfill(5),
        system="STESTS",
        sub_system=sub_system.name,
        timestamp=datetime.datetime.utcnow().isoformat(),
    )
