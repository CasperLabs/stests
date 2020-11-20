from stests.core.types.orchestration import ExecutionContext
from stests.generators.wg_110 import args
from stests.generators.wg_110 import phase_1



# Workload custom args.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Dispatches transfers in volume."

# Set of workflow phases.
PHASES = (
    phase_1,
)

# Workload type.
TYPE = "WG-110"

# Workload typeset - registered with encoder.
TYPE_SET = {
    Arguments,
}