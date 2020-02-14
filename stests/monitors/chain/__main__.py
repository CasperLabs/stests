from stests.core import cache
from stests.core import mq
from stests.core.utils import factory



# Initialise MQ sub-package.
mq.initialise(mq.BrokerMode.MONITORING)
import stests.monitors.chain.actors


# Iterate networks & raise begin monitoring event.
from stests.monitors.chain.actors.blocks import do_monitor_blocks
for network in cache.get_networks():
    network_id = factory.create_network_id(network.name)
    do_monitor_blocks.send(network_id)
