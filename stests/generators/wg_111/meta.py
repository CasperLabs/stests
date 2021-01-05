from stests.core.types.orchestration import ExecutionContext
from stests.generators.wg_111 import args
from stests.generators.wg_111 import p1s1_do_transfers



# Workload custom args.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Dispatches a set of fire & forget transfers."

# Set of workflow phases.
PHASES = (
    (p1s1_do_transfers, ),
    )

# Workload type.
TYPE = "WG-111"

# Workload typeset - registered with encoder.
TYPE_SET = {
    Arguments,
}
