# Initialise broker.
from stests.core import mq
mq.initialise()

# Initialise encoder.
from stests.core.mq import encoder
encoder.initialise()

# Import actors: monitoring.
import stests.monitoring.control
import stests.monitoring.events

# Start monitoring.
from stests.monitoring.control import do_start_monitoring
do_start_monitoring.send()
