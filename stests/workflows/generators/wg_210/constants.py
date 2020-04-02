# --------------------------------------------------------------------
# METADATA
# --------------------------------------------------------------------

# Workload description.
DESCRIPTION = "Counter call / define"

# Workload type.
TYPE = "WG-210"

# Message queue.
QUEUE = f"workflows.generators.{TYPE}"

# --------------------------------------------------------------------
# DEFAULTS
# --------------------------------------------------------------------

# Default faucet's initial CLX balance.
FAUCET_INITIAL_CLX_BALANCE = int(1e11)

# Default number of times counters will be incremented.
INCREMENTS = 3

# Default number of user accounts to generate.
USER_ACCOUNTS = 5

# Default user's CLX balance.
USER_INITIAL_CLX_BALANCE = int(1e8)

# --------------------------------------------------------------------
# ACCOUNT OFFSETS
# --------------------------------------------------------------------

# Account index: network faucet.
ACC_NETWORK_FAUCET = 0

# Account index: run faucet.
ACC_RUN_FAUCET = 1

# Account index: run users.
ACC_RUN_USERS = 2
