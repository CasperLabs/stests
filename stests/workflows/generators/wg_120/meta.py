from stests.core.types.orchestration import ExecutionContext
from stests.workflows.generators.wg_120 import args
from stests.workflows.generators.wg_120 import phase_1
from stests.workflows.generators.wg_120 import phase_2


# Workload custom args.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Token Transfers (wasm-less)"

# Set of workflow phases.
PHASES = (
    phase_1,
    phase_2,
)

# Workload type.
TYPE = "WG-120"

# Workload typeset - registered with encoder.
TYPE_SET = {
    Arguments,
}

