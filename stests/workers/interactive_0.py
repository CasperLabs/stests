from stests.workers.utils import setup_interactive
from stests.workers.utils import start_monitoring
from stests.workers.utils import start_workflows



# Setup.
setup_interactive()

# Start workload generators.
start_workflows()

# Start chain monitoring.
start_monitoring()
