from stests.workflows.generators.wg_100.args import Arguments
from stests.workflows.generators.wg_100.args import ARGS
from stests.workflows.generators.wg_100.constants import DESCRIPTION
from stests.workflows.generators.wg_100.constants import TYPE
from stests.workflows.generators.wg_100 import phase_1
from stests.workflows.generators.wg_100 import phase_2



# Type set to be registered with encoder.
TYPE_SET = {
    Arguments,
}

# Set of workflow phases.
PHASES = (
    phase_1,
    phase_2,
)