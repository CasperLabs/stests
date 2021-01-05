from stests.core.types.orchestration import ExecutionContext
from stests.generators.wg_201 import args
from stests.generators.wg_201 import p1s1_withdraw_bid



# Workload custom args type.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Dispatches an auction withdraw bid deploy."

# Workflow phases/steps.
PHASES = (
    (p1s1_withdraw_bid, ),
)

# Workload type.
TYPE = "WG-201"

# Workload typeset - registered when encoder.initialise is invoked.
TYPE_SET = {
    Arguments,
}
