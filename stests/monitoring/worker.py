# Initialise broker.
from stests.core import mq
mq.initialise()

# Import actors: monitoring.
import stests.monitoring.events
import stests.monitoring.manager

# Start monitoring.
from stests.monitoring.manager import do_start_monitoring
do_start_monitoring.send()
