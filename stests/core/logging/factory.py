import datetime
import uuid

from stests.core.logs.types import LogLevel
from stests.core.logs.types import LogInfoMetadata
from stests.core.logs.types import MonitoringEventLogInfo
from stests.core.logs.types import SubSystem
from stests.core.logs.types import WorkflowEventLogInfo

from stests.core.types.infra import NodeEventType
from stests.core.types.orchestration import ExecutionEventType



def get_monitoring_log_event(
    event_id: str,
    event_type: NodeEventType,
    node_index: int,
    block_hash: str = None,
    deploy_hash: str = None,
    message: str = None,
    log_level: LogLevel = LogLevel.INFO,
    priority: int = 5,
    ) -> MonitoringEventLogInfo:
    """Returns chain related log event information.
    
    """
    return MonitoringEventLogInfo(
        block_hash=block_hash,
        deploy_hash=deploy_hash,
        node_index=node_index,
        message=message,
        meta=_get_metadata(
            event_id=event_id,
            event_type=event_type.name,
            log_level=log_level,
            priority=priority,
            sub_system=SubSystem.CHAIN,
        )
    )


def get_workflow_log_event(
    event_id: str,
    event_type: ExecutionEventType,
    node_index: int,
    message: str = None,
    log_level: LogLevel = LogLevel.INFO,
    priority: int = 5,
    ) -> WorkflowEventLogInfo:
    """Returns workflow related log event information.
    
    """
    return MonitoringEventLogInfo(
        node_index=node_index,
        message=message,
        meta=_get_metadata(
            event_id=event_id,
            event_type=event_type.name,
            log_level=log_level,
            priority=priority,
            sub_system=SubSystem.WFLOW,
        )
    )


def _get_metadata(
    event_id: int,
    event_type: str,
    log_level: LogEventLevel,
    priority: int,
    sub_system: LogEventSubSystem,
    ) -> LogInfoMetadata:
    """Returns log event metadata.
    
    """
    return LogInfoMetadata(
        event_id=event_id,
        event_type=event_type,
        event_uid=str(uuid.uuid4()),
        host_name="get-machine",
        log_level=log_level,
        priority=priority,
        process_id="get-process-id",
        process_name="get-process-name",
        system="STESTS",
        sub_system=sub_system.name,
        thread_id="get-thread-id",
        timestamp=datetime.datetime.now(),
    )
