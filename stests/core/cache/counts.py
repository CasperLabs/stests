from stests.core.domain import RunContext
from stests.core.cache.utils import do_incrby
from stests.core.cache.utils import pull_count



@do_incrby
def increment_step_deploy_count(ctx: RunContext):
    """Increments (atomically) count of run step deploys.

    :param ctx: Generator run contextual information.

    """
    return [
        "run-step-deploy-count",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        ctx.run_step,
    ]


@pull_count
def get_step_deploy_count(ctx: RunContext) -> int:
    """Reurns current count of run step deploys.

    :param ctx: Generator run contextual information.

    """
    return [
        "run-step-deploy-count",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        ctx.run_step,
    ]
