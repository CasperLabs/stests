from stests.core.domain import ContractType


# Type of contract.
TYPE = ContractType.COUNTER_DEFINE_STORED

# Wasm file name.
WASM = "counter_define_stored.wasm"

# Name of contract - see use when passed as session-name.
NAME = "counter"

# Flag indicating whether this contract can be installed under a single account and invoked by other accounts.
IS_SINGLETON = False
