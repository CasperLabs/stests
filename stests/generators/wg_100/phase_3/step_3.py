from stests.core.orchestration import ExecutionRunInfo
from stests.core.utils import logger



# Step description.
DESCRIPTION = "Dispatches a notification to signal that generator has completed."

# Step label.
LABEL = "notify-competion"


def execute(ctx: ExecutionRunInfo):
    """Step entry point.
    
    :param ctx: Generator run contextual information.

    """      
    # TODO: push notification.
    logger.log(f"ACTOR :: {ctx.run_type} :: R-{str(ctx.run_index).zfill(3)} has completed")
