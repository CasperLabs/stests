# --------------------------------------------------------------------
# METADATA
# --------------------------------------------------------------------

# Workload description.
DESCRIPTION = "ERC-20 Token Auction"

# Workload type.
TYPE = "WG-100"

# --------------------------------------------------------------------
# DEFAULTS
# --------------------------------------------------------------------

# Default contract's initial CLX balance = 1m.
CONTRACT_INITIAL_CLX_BALANCE = int(1e7)

# Default faucet's initial CLX balance = 10m.
FAUCET_INITIAL_CLX_BALANCE = int(1e10)

# Default name of ERC20 token for which an auction is being simulated.
TOKEN_NAME = "ABC"

# Default supply of ERC20 token = 20k.
TOKEN_SUPPLY = int(2e4)

# Default number of user accounts to generate.
USER_ACCOUNTS = 5

# Default number of bids to submit per user account.
USER_BIDS = 1

# Default user's CLX balance = 1m.
USER_INITIAL_CLX_BALANCE = int(1e7)

# Default name of the contract's wasm blob.
WASM_CONTRACT_FILENAME = "erc20_smart_contract.wasm"
