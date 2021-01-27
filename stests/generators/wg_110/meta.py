from stests.core.types.orchestration import ExecutionContext
from stests.generators.wg_110 import args
from stests.generators.wg_110 import p1s1_set_accounts
from stests.generators.wg_110 import p2s1_fund_faucet
from stests.generators.wg_110 import p2s2_fund_users
from stests.generators.wg_110 import p3s1_refund_users
from stests.generators.wg_110 import p3s2_refund_faucet


# Workload custom args type.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Dispatches transfers in volume."

# Workflow phases/steps.
PHASES = (
    (p1s1_set_accounts,),
    (p2s1_fund_faucet, p2s2_fund_users,),
    (p3s1_refund_users, p3s2_refund_faucet,),
)

# Workload type.
TYPE = "WG-110"

# Workload typeset - registered when encoder.initialise is invoked.
TYPE_SET = {
    Arguments,
}
