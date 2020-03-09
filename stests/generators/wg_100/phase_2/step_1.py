from stests.core.orchestration import ExecutionContext
from stests.core.utils import resources
from stests.generators.wg_100 import constants


# Step description.
DESCRIPTION = "Deploys ERC-20 contract"

# Step label.
LABEL = "deploy-contract"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print("TODO: deploy erc-20 contract")


