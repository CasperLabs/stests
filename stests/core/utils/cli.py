import os
import sys
import typing
from datetime import datetime

from beautifultable import BeautifulTable



# BeautifulTable is emitting several warnings - these are to be suppressed until resolved.
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


# Set of logging levels.
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARN'


def get_table(cols, rows, max_width=1080) -> BeautifulTable:
    """Returns a table ready for printing to stdout.
    
    :param cols: Table columns.
    :param rows: Table rows.
    :param max_width: Maximum table width in characters.

    """
    # Set table data.
    t = BeautifulTable(max_width=max_width)
    t.column_headers = cols
    for row in rows:
        t.append_row(row)

    # Set default style.
    t.set_style(BeautifulTable.STYLE_NONE)
    t.top_border_char = "-"
    t.header_separator_char = '-'
    t.bottom_border_char = "-"

    return t    


def log(msg: str = None, level: str = LOG_LEVEL_INFO):
    """Outputs a message to log.

    :param str msg: Message to be written to log.
    :param str level: Message level (e.g. INFO).

    """
    print(_get_message(msg, level))


def log_line():
    """Outputs a message to log.

    :param str msg: Message to be written to log.
    :param str level: Message level (e.g. INFO).

    """
    print("------------------------------------------------------------------------------------------------------------------------------------")


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