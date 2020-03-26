from stests.generators.wg_200.args import Arguments
from stests.generators.wg_200.args import ARGS
from stests.generators.wg_200.constants import DESCRIPTION
from stests.generators.wg_200.constants import TYPE
from stests.generators.wg_200 import phase_1
from stests.generators.wg_200 import phase_2
from stests.generators.wg_200 import phase_3



# Type set to be registered with encoder.
TYPE_SET = {
    Arguments,
}

# Set of workflow phases.
PHASES = (
    phase_1,
    phase_2,
    phase_3,
)
