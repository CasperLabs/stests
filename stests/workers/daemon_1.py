from stests.workers.utils import setup_daemon
from stests.workers.utils import start_orchestration



# Setup.
setup_daemon()

# Start workload generators.
start_orchestration()
