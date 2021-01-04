from stests.core.types.orchestration import ExecutionContext
from stests.generators.wg_100 import args
from stests.generators.wg_100 import phase_1
from stests.generators.wg_100 import phase_2
from stests.generators.wg_100 import phase_3


# Workload custom args.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Dispatches transfers in volume."

# Set of workflow phases.
PHASES = (
    phase_1,
    phase_2,
    phase_3,
    )

# Workload type.
TYPE = "WG-100"

# Workload typeset - registered with encoder.
TYPE_SET = {
    Arguments,
}
