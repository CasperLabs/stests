from stests.core import cache
from stests.core import mq
from stests.core.utils import factory



# Import MQ sub-package & initialise.
mq.initialise(mq.BrokerMode.MONITORING)

# Iterate networks & raise begin monitoring event.
from stests.monitors.chain import do_monitor_blocks
for network in cache.get_networks():
    network_id = factory.create_network_id(network.name)
    do_monitor_blocks.send(network_id)
