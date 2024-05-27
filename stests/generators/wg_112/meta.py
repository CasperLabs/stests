from stests.core.types.orchestration import ExecutionContext
from stests.generators.wg_112 import args
from stests.generators.wg_112 import p1s1_do_transfers_v2



# Workload custom args type.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Dispatches a set of fire & forget transfers."

# Workflow phases/steps.
PHASES = (
    (p1s1_do_transfers_v2, ),
    )

# Workload type.
TYPE = "WG-112"

# Workload typeset - registered when encoder.initialise is invoked.
TYPE_SET = {
    Arguments,
}
