from stests.core.types.orchestration import ExecutionContext
from stests.generators.wg_211 import args
from stests.generators.wg_211 import p1s1_set_accounts
from stests.generators.wg_211 import p1s2_fund_users
from stests.generators.wg_211 import p1s3_delegate
from stests.generators.wg_211 import p2s1_await_eras
from stests.generators.wg_211 import p2s2_undelegate



# Workload custom args type.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Tests the auction contract by submitting batches of delegation/undelegation requests."

# Workflow phases/steps.
PHASES = (
    (p1s1_set_accounts, p1s2_fund_users, p1s3_delegate, ),
    (p2s1_await_eras, p2s2_undelegate, ),
)

# Workload type.
TYPE = "WG-211"

# Workload typeset - registered when encoder.initialise is invoked.
TYPE_SET = {
    Arguments,
}
