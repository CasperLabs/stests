# Reuse wg_100 phase 1 & 3.
from stests.orchestration.generators.wg_100 import meta as wg_100

from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.wg_200 import args
from stests.orchestration.generators.wg_200 import phase_2



# Workload custom args.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Counter (client contract)"

# Set of workflow phases.
PHASES = (
    wg_100.phase_1,
    phase_2,
    wg_100.phase_2,
)

# Workload type.
TYPE = "WG-200"

# Workload typeset - registered with encoder.
TYPE_SET = {
    Arguments,
}

