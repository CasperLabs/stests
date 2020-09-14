import dataclasses
import sys
from datetime import datetime

from stests.core.types.logging import LogMessage
from stests.core.types.logging import OutputMode



def log_event(msg: LogMessage, mode: OutputMode):
    """Appends event information to event log.

    :param msg: Message to be logged.
    :param mode: Logging output mode as per execution host.

    """
    if mode == OutputMode.INTERACTIVE:
        if msg.event.priority > 1:
            print(f"[{datetime.utcnow().isoformat()}Z] [PID {msg.process.pid}] [{msg.app.system}] [{msg.event.level}] {msg.message}",
                  file=sys.stderr if msg.event.priority > 9 else sys.stdout)
    else:
        print(f"[{datetime.utcnow().isoformat()}Z] [PID {msg.process.pid}] [{msg.app.system}] [{msg.event.level}] {msg.message}",
                file=sys.stderr if msg.event.priority > 9 else sys.stdout)
