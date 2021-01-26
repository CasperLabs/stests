import typing

from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import constants
from stests.generators.utils import verification



# Step label.
LABEL = "cleanup"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    cache.state.delete_by_run(ctx)
