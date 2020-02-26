from stests.core import cache
from stests.core import mq
from stests.core.utils import factory



# Initialise MQ sub-package.
mq.initialise()
from stests.monitoring.chain import do_monitor_blocks

# Iterate networks & wire upto streaming events.
for network in cache.get_networks():
    network_id = factory.create_network_id(network.name)
    for node in cache.get_nodes(network):
        node_id = factory.create_node_id(network_id, node.index)
        do_monitor_blocks.send(node_id)
        # break
