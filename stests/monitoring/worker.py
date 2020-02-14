# Import MQ sub-package & initialise.
from stests.core import mq
mq.initialise(mq.BrokerMode.MONITORING)

# Import actors.
import stests.monitoring.chain.actors
