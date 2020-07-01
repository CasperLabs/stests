import dataclasses
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
            print(f"[{datetime.utcnow().isoformat()}Z] [PID {msg.process.pid}] [{msg.app.system}] [{msg.event.level}] {msg.message}")
    else:
        print(f"[{datetime.utcnow().isoformat()}Z] [PID {msg.process.pid}] [{msg.process.host}] [{msg.event.level}] [{msg.event.priority}] [{msg.app.company.lower()}-{msg.app.system.lower()}] [{msg.app.sub_system.lower()}] payload={dataclasses.asdict(msg)}")
