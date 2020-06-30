from stests.core.types.orchestration import ExecutionContext
from stests.workflows.generators.wg_1000 import args
from stests.workflows.generators.wg_1000 import phase_1
from stests.workflows.generators.wg_1000 import phase_2


# Workload custom args.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Executes simple node-rs deploy mock"

# Set of workflow phases.
PHASES = (
    phase_1,
    phase_2,
)

# Workload type.
TYPE = "WG-1000"

# Workload typeset - registered with encoder.
TYPE_SET = {
    Arguments,
}

