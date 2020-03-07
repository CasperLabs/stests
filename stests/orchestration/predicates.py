from stests.core import cache
from stests.core.cache.locks import RunLock
from stests.core.cache.locks import RunPhaseLock
from stests.core.cache.locks import RunStepLock
from stests.core.domain import RunContext
from stests.core.utils import logger
from stests.orchestration.model import Workflow



def can_start_run(ctx: RunContext) -> bool:
    """Returns flag indicating whether a run increment is valid.
    
    """
    # False if workflow unregistered.
    try:
        Workflow.create(ctx)
    except ValueError:
        logger.log_warning(f"unregistered workflow: {ctx.run_type}")
        return False

    # False if cannot acquire lock.
    lock = RunLock(
        ctx.network,
        ctx.run_index,
        ctx.run_type
    )
    _, acquired = cache.control.lock_run(lock)
    if not acquired:
        logger.log_warning(f"unacquired run lock: {ctx.run_type} :: run={ctx.run_index}")
        return False

    # All tests passed, therefore return true.    
    return True


def can_start_phase(ctx: RunContext, phase_index: int) -> bool:
    """Returns flag indicating whether a phase increment is valid.
    
    """
    # False if workflow unregistered.
    try:
        workflow = Workflow.create(ctx)
    except ValueError:
        return False

    # False if phase index is invalid.
    if phase_index > len(workflow.phases):
        logger.log_warning(f"invalid phase index: {ctx.run_type} :: run={ctx.run_index} :: phase={phase_index}")
        return False
    
    # False if cannot acquire lock.
    lock = RunPhaseLock(
        ctx.network,
        ctx.run_index,
        ctx.run_type,
        phase_index
    )
    _, acquired = cache.control.lock_phase(lock)
    if not acquired:
        logger.log_warning(f"unacquired phase lock: {ctx.run_type} :: run={ctx.run_index} :: phase={phase_index}")
        return False
    
    # All tests passed, therefore return true.    
    return True


def can_start_step(ctx: RunContext, phase_index: int, step_index: int) -> bool:
    """Returns flag indicating whether a step increment is valid.
    
    """
    # False if workflow unregistered.
    try:
        workflow = Workflow.create(ctx)
    except ValueError:
        return False

    # False if phase index is invalid.
    if phase_index > len(workflow.phases):
        logger.log_warning(f"invalid phase index: {ctx.run_type} :: {ctx.run_index_label} :: phase={phase_index}")
        return False
    
    # False if step index is invalid.
    phase = workflow.phases[phase_index - 1]
    if step_index > len(phase.steps):
        logger.log_warning(f"invalid step index: {ctx.run_type} :: {ctx.run_index_label} :: phase={phase_index} :: step={step_index}")
        return False

    # False if cannot acquire lock.
    lock = RunStepLock(
        ctx.network,
        ctx.run_index,
        ctx.run_type,
        phase_index,
        step_index
    )
    _, acquired = cache.control.lock_step(lock)
    if not acquired:
        logger.log_warning(f"unacquired step lock: {ctx.run_type} :: run={ctx.run_index} :: phase={phase_index} :: step={step_index}")
        return False
    
    # All tests passed, therefore return true.    
    return True