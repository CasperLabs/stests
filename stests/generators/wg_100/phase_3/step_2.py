from stests.core.domain import RunContext
from stests.generators.wg_100 import constants
from stests.generators.wg_100.phase_3 import utils



# Step description.
DESCRIPTION = "Refunds funds previously transferred from network faucet."

# Step label.
LABEL = "refund-network-faucet"


def execute(ctx: RunContext):
    """Step entry point.
    
    :param ctx: Generator run contextual information.

    """     
    utils.do_refund.send(
        ctx,
        constants.ACC_RUN_FAUCET,
        constants.ACC_NETWORK_FAUCET
    )
