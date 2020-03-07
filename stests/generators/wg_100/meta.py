from stests.generators.wg_100.args import Arguments

from stests.generators.wg_100.constants import DESCRIPTION
from stests.generators.wg_100.constants import TYPE

from stests.generators.wg_100 import phase_1
from stests.generators.wg_100 import phase_2
from stests.generators.wg_100 import phase_3



TYPE_SET = {
    Arguments,
}

PHASES = (
    phase_1,
    phase_2,
    phase_3,
)

PIPELINE = (
    phase_1.step_1,
    phase_1.step_2,
    phase_1.step_3,
    phase_1.step_4,
    phase_1.step_5,
    phase_2.step_1,
    phase_2.step_2,
    phase_3.step_1,
    phase_3.step_2,
    phase_3.step_3,
)
