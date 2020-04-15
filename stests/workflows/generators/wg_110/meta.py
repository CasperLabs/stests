# Note - import wg_100 actors as we are basically running
# the same workflow but with a different parameterisation.
from stests.workflows.generators.wg_100 import meta as wg_100



# Workload custom args.
Arguments = wg_100.Arguments

# Workload command line args.
ARGS = wg_100.ARGS

# Workload description.
DESCRIPTION = "Token Transfers (stored contract)"

# Set of workflow phases.
PHASES = wg_100.PHASES

# Workload type.
TYPE = "WG-110"

# Workload typeset - registered with encoder.
TYPE_SET = wg_100.TYPE_SET
