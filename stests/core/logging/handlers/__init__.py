import typing

from stests.core.logging.handlers import stdout
from stests.core.logging.handlers import lstash
from stests.core.types.logging import OutputMode
from stests.core.utils import env
from stests.core.utils.exceptions import InvalidEnvironmentVariable



# Environment variables required by this module.
class EnvVars:
    # Logging target.
    TYPE = env.get_var("LOGGING_TYPE", "STDOUT")


# Map: Logging handler type -> handler.
HANDLERS = {
    "STDOUT": stdout,
    "LOGSTASH": lstash,
}


def get_handler(mode: OutputMode) -> typing.Callable:
    """Returns logging output handler matching STESTS_LOGGING_TYPE environment variable 
    unless output mode is interactive in which case dfault handler is returned.

    :param mode: The mode of output as per the current execution container.

    :returns: A configured logging output handler.

    """
    if mode == OutputMode.INTERACTIVE:
        return stdout
    else:
        try:
            return HANDLERS[EnvVars.TYPE]
        except KeyError:
            raise InvalidEnvironmentVariable("LOGGING_TYPE", EnvVars.TYPE, HANDLERS)
