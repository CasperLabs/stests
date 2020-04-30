from datetime import datetime
import os
import typing



# Set of logging levels.
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARN'


def log(msg: str = None, level: str = LOG_LEVEL_INFO):
    """Outputs a message to log.

    :param str msg: Message to be written to log.
    :param str level: Message level (e.g. INFO).

    """
    print(_get_message(msg, level))


def log_warning(err: typing.Union[str, Exception]):
    """Logs a runtime warning.

    :param str err: Warning to be written to log.

    """
    if issubclass(BaseException, err.__class__):
        msg = f"{err.__class__} :: {err}"
    else:
        msg = f"{err}"
    log(msg, LOG_LEVEL_WARNING)


def _get_message(msg: str, level: str) -> str:
    """Returns formatted logging message.

    """
    if msg is None:
        return _NULL_MSG

    timestamp = datetime.utcnow().isoformat()
    pid = str(os.getpid()).zfill(5)

    return f"{timestamp}Z [{level}] [{pid}] STESTS :: {str(msg).strip()}"