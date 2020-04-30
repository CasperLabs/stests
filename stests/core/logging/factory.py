import datetime
import os
import platform
import pwd
import socket
import typing
import uuid

from stests.core.logging.enums import CoreEventType
from stests.core.logging.enums import MonitoringEventType
from stests.core.logging.enums import WorkflowEventType
from stests.core.logging.types import ApplicationInfo
from stests.core.logging.types import EventInfo
from stests.core.logging.types import Level
from stests.core.logging.types import LogMessage
from stests.core.logging.types import ProcessInfo
from stests.core.logging.types import SubSystem

from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext



def get_core_event_info(
    event_type: CoreEventType,
    message: str = None,
    ) -> LogMessage:
    """Returns monitoring related log event information.
    
    """
    event_id=event_type.value
    is_error = event_type in (
        CoreEventType.ACTOR_ERROR,
        )
    is_warning = event_type in (
        CoreEventType.ENCODING_ERROR,
        )
    message=f"{event_type.name} :: {str(message)}" if message else event_type.name
    level = Level.ERROR if is_error else Level.WARN if is_warning else Level.INFO
    priority=9 if is_error else 7 if is_warning else 5

    return LogMessage(
        app=_get_app_info(SubSystem.CORE),
        event=_get_event_info(event_id, level, priority, event_type),
        process=_get_process_info(),
        message=message,
        data=dict()
    )


def get_monitoring_event_info(
    event_type: MonitoringEventType,
    node: typing.Union[Node, NodeIdentifier],
    message: str = None,
    event_id: str = None,
    block_hash: str = None,
    deploy_hash: str = None,
    ) -> LogMessage:
    """Returns monitoring related log event information.
    
    """
    event_id=event_id or event_type.value
    is_error = event_type in (
        MonitoringEventType.DEPLOY_DISCARDED,
        MonitoringEventType.DEPLOY_ORPHANED,
        MonitoringEventType.API_ERROR,
        )
    is_warning = event_type in (
        MonitoringEventType.ACCOUNT_NOT_FOUND,
        MonitoringEventType.BLOCK_NOT_FOUND,
        MonitoringEventType.DEPLOY_REQUEUED,
        )
    message=f"{event_type.name} :: {str(message)}" if message else event_type.name
    level = Level.ERROR if is_error else Level.WARN if is_warning else Level.INFO
    priority=9 if is_error else 7 if is_warning else 5

    return LogMessage(
        app=_get_app_info(SubSystem.MONITORING),
        event=_get_event_info(event_id, level, priority, event_type),
        process=_get_process_info(),
        message=message,
        data={i:j for i, j in {
            'network': node.network_name,
            'node': node.label_index,
            'block': block_hash,
            'deploy': deploy_hash,
        }.items() if j is not None}
    )


def get_workflow_event_info(
    event_type: WorkflowEventType,
    ctx: ExecutionContext,
    message: typing.Union[BaseException, str] = None,
    ) -> LogMessage:
    """Returns workflow related log event information.
    
    """
    event_id=event_type.value
    is_error = event_type in (
        WorkflowEventType.RUN_ERROR,
        WorkflowEventType.PHASE_ERROR,
        WorkflowEventType.STEP_ERROR,
        )
    is_warning = event_type in (
        WorkflowEventType.RUN_ABORT,
        WorkflowEventType.PHASE_ABORT,
        WorkflowEventType.STEP_ABORT,
        WorkflowEventType.STEP_FAILURE,
        )
    message=f"{event_type.name} :: {str(message)}" if message else event_type.name
    level = Level.ERROR if is_error else Level.WARN if is_warning else Level.INFO
    priority=9 if is_error else 7 if is_warning else 5

    return LogMessage(
        app=_get_app_info(SubSystem.WORKFLOW),
        event=_get_event_info(event_id, level, priority, event_type),
        process=_get_process_info(),
        message=message,
        data={i:j for i, j in {
            'network': ctx.network,
            'phase_index': ctx.phase_index,
            'run_index': ctx.run_index,
            'run_type': ctx.run_type,
            'step_index': ctx.step_index,
            'step_label': ctx.step_label,  
        }.items() if j is not None}
    )


def _get_app_info(sub_system: SubSystem) -> ApplicationInfo:
    """Returns application information to be logged.
    
    """
    return ApplicationInfo("STESTS", sub_system.name)


def _get_event_info(
    event_id: str,
    level: Level,
    priority: int,
    type: typing.Union[CoreEventType, MonitoringEventType, WorkflowEventType]
    ) -> EventInfo:
    """Returns event information to be logged.
    
    """
    return EventInfo(
        id=event_id,
        level=level.name,
        priority=priority,
        timestamp=datetime.datetime.utcnow().isoformat(),
        type=type.name,
        uid=str(uuid.uuid4()),
        )


def _get_process_info() -> ProcessInfo:
    """Returns process information to be logged.
    
    """
    return ProcessInfo(
        host=socket.gethostname(),
        net=platform.node(),
        os_user=pwd.getpwuid(os.getuid())[0],
        pid=str(os.getpid()).zfill(5),
        )
