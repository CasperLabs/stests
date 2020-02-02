from stests.core import mq
from stests.core.utils import encoder
from stests.generators.wg_100.phase_01.generator_ctx import Context



# Framework requirement: register context with encoder.
encoder.register_type(Context)

# Framework requirement: initialise broker.
mq.init_broker()

# Import actors.
from stests.generators.wg_100.phase_01.actors import accounts
from stests.generators.wg_100.phase_01.actors import contract
