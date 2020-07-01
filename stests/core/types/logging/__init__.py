from stests.core.types.logging.application_info import ApplicationInfo
from stests.core.types.logging.enums import Level
from stests.core.types.logging.enums import OutputMode
from stests.core.types.logging.enums import ENUM_SET
from stests.core.types.logging.event_info import EventInfo
from stests.core.types.logging.message import LogMessage
from stests.core.types.logging.process_info import ProcessInfo



TYPE_SET = {
    ApplicationInfo,
    EventInfo,
    LogMessage,
    ProcessInfo,
} | ENUM_SET
