import typing

from stests.core.cache.locks import RunStepLock
from stests.core.cache.utils import encache_lock



@encache_lock
def lock_run_step(lock: RunStepLock) -> typing.Tuple[typing.List[str], RunStepLock]:
    """Encaches a lock: RunStepLock.

    :param lock: Information to be locked.

    :returns: A cached account.

    """
    return [
        "lock-run-step",
        lock.network,
        lock.run_type,
        f"R-{str(lock.run_index).zfill(3)}",
        lock.step
    ], lock
