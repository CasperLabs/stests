from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.wg_100 import args
from stests.orchestration.generators.wg_100 import phase_1
from stests.orchestration.generators.wg_100 import phase_2


# Workload custom args.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Token Transfers (off-chain contract)"

# Set of workflow phases.
PHASES = (
    phase_1,
    phase_2,
)

# Workload type.
TYPE = "WG-100"

# Workload typeset - registered with encoder.
TYPE_SET = {
    Arguments,
}

