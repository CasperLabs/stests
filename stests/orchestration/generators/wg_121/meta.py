from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.wg_121 import args
from stests.orchestration.generators.wg_121 import phase_1
from stests.orchestration.generators.wg_121 import phase_2


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
TYPE = "WG-121"

# Workload typeset - registered with encoder.
TYPE_SET = {
    Arguments,
}

