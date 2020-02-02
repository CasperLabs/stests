from stests.core import mq
from stests.core.utils import encoder
from stests.core.utils import env
from stests.generators.wg_100.phase_01.workflow import Context



# Framework requirement: register arguments type.
encoder.register_type(Arguments)

# Framework requirement: initialise broker.
mq.init_broker(env.get_network_id())

# Import actors.
from stests.generators.wg_100.phase_01.actors import accounts
from stests.generators.wg_100.phase_01.actors import contract
