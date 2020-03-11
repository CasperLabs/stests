# Import initialiser to setup upstream services / actors.
import stests.initialiser

# Start monitoring.
from stests.monitoring.chain import launch_stream_monitors
launch_stream_monitors.send()
