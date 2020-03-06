from stests.core.domain import RunContext
from stests.core.utils import resources
from stests.generators.wg_100 import constants


# Step description.
DESCRIPTION = "Initialises cache"

# Step label.
LABEL = "init-cache"


def execute(ctx: RunContext):
    """Step entry point.
    
    :param ctx: Generator run contextual information.

    """
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print("TODO: deploy erc-20 contract")


