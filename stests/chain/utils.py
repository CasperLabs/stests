import functools
import pathlib
import typing

from stests.core.utils.env import get_var
from stests.core.utils.misc import Timer
from stests.events import EventType



def execute_cli(
    command: str,
    on_failure_event: EventType, 
    max_attempts: int = 5,
    retry_delay: float = float(1),
    ) -> typing.Callable:
    """Decorator to orthoganally execute a CLI operation.

    :param command: CLI command being executed.
    :param failure_event_type: Logging event to emit upon failure.
    :param max_attempts: Maximum attempts to try being escaping.
    :param retry_delay: Retry delay.

    :returns: Decorated function with it's result augmented with execution stats.
    
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            with Timer() as timer:
                attempts = 0
                while attempts < max_attempts:
                    attempts += 1
                    try:
                        result = func(*args, **kwargs)
                    except Exception as err:
                        if attempts == max_attempts:
                            raise Exception(f"{command} failed {max_attempts} times - {err}")
                        log_event(on_failure_event, f"try {attempts} failed - retrying")
                        time.sleep(retry_delay)
                    else:
                        break

            return result, timer.elapsed, attempts

        return wrapper
    return decorator


def get_contract_path(wasm_filename: str) -> pathlib.Path:
    """Returns a path to a smart contract.

    :param wasm_filename: Name of wasm file to be loaded into memory.

    :returns: Path to a wasm blob.
    
    """
    # Return wasm at path specified by env var.
    path = pathlib.Path(get_var("PATH_WASM")) / wasm_filename    
    if path.exists():
        return path

    raise ValueError("WASM file could not be found. Verify the STESTS_PATH_WASM env var setting.")