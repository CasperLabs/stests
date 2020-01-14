from stests.core.types import factory
from stests.core.types import account
from stests.core.types import core
from stests.core.types import network
from stests.core.types import node

# Set: supported domain classes.
CLASSES = \
    account.CLASSES | \
    core.CLASSES | \
    network.CLASSES | \
    node.CLASSES

# Set: supported domain enums.
ENUMS = \
    account.ENUMS | \
    network.ENUMS | \
    node.ENUMS

# Set: supported domain types.
TYPESET = CLASSES | ENUMS
