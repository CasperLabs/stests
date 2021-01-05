from stests.core.types.orchestration import ExecutionContext
from stests.generators.wg_200 import args
from stests.generators.wg_200 import p1s1_submit_bid



# Workload custom args type.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Dispatches an auction submit bid deploy."

# Workflow phases/steps.
PHASES = (
    (p1s1_submit_bid, ),
)

# Workload type.
TYPE = "WG-200"

# Workload typeset - registered when encoder.initialise is invoked.
TYPE_SET = {
    Arguments,
}
