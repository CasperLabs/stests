import os
import platform
import pwd
import socket

from stests import __version__
from stests.core.types.logging import ApplicationInfo
from stests.core.types.logging import EventInfo
from stests.core.types.logging import Level
from stests.core.types.logging import LogMessage
from stests.core.types.logging import ProcessInfo

from stests import events



def get_message(info: events.EventInfo) -> LogMessage:
    """Returns application information to be logged.
    
    """
    if info.priority >= Level.FATAL.value:
        level = Level.FATAL
    elif info.priority >= Level.CRITICAL.value:
        level = Level.CRITICAL
    elif info.priority >= Level.ERROR.value:
        level = Level.ERROR
    elif info.priority >= Level.WARN.value:
        level = Level.WARN
    elif info.priority >= Level.INFO.value:
        level = Level.INFO
    else:
        level = Level.DEBUG

    from stests.core.utils import encoder

    return LogMessage(
        app=ApplicationInfo(
            "CASPERLABS",
            "STESTS",
            info.sub_system,
            __version__
        ),
        event=EventInfo(
            id=info.id,
            level=level.name,
            priority=info.priority,
            timestamp=info.timestamp,
            type=info.name,
            uid=info.uid,
        ),
        process=ProcessInfo(
            host=socket.gethostname(),
            net=platform.node(),
            os_user=pwd.getpwuid(os.getuid())[0],
            pid=str(os.getpid()).zfill(5),
        ),
        message = info.message,
        data=encoder.encode(info.data, requires_decoding=False),
    )
