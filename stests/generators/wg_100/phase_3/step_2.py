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


def verify_deploy(ctx: RunContext, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Generator run contextual information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, dhash)
    utils.verify_refund(ctx, dhash)
    utils.verify_deploy_count(ctx, 1)
