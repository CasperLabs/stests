from stests.generators.wg_100.phase_3.actors import do_refund_step_1
from stests.generators.wg_100.phase_3.actors import do_refund_step_2
from stests.generators.wg_100.phase_3.actors import do_notify_completion

from stests.generators.wg_100.phase_3.verifiers import verify_refund_step_1
from stests.generators.wg_100.phase_3.verifiers import verify_refund_step_2

from stests.generators.wg_100.phase_3 import step_1
from stests.generators.wg_100.phase_3 import step_2
from stests.generators.wg_100.phase_3 import step_3


# Set: steps to be executed.
STEPS = (
    step_1,
    step_2,
    step_3,
)
