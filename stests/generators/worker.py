# Import MQ sub-package & initialise.
from stests.core import mq
mq.initialise(mq.BrokerMode.SIMULATION)

# WG-100.
import stests.generators.wg_100.args
import stests.generators.wg_100.actors
