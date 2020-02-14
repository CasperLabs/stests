from stests.core import mq


# Import MQ sub-package & initialise.
mq.initialise(mq.BrokerMode.MONITORING)

# Import actors.
import stests.monitoring.chain.actors

