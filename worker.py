# Import initialiser to setup upstream services / actors.
import stests.initialiser

# Start monitoring.
from stests.monitoring.manager import do_start_monitoring
do_start_monitoring.send()
