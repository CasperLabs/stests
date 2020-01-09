from stests.core.types import factory
from stests.core.types import account
from stests.core.types import core
from stests.core.types import network
from stests.core.types import node

# Set: supported domain types.
TYPESET = \
    account.TYPESET | \
    core.TYPESET | \
    network.TYPESET | \
    node.TYPESET
