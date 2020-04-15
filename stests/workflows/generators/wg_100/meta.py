from stests.core.orchestration import ExecutionContext
from stests.workflows.generators.wg_100.args import Arguments
from stests.workflows.generators.wg_100.args import ARGS
from stests.workflows.generators.wg_100.constants import DESCRIPTION
from stests.workflows.generators.wg_100.constants import TYPE
from stests.workflows.generators.wg_100 import phase_1
from stests.workflows.generators.wg_100 import phase_2



# Type set to be registered with encoder.
TYPE_SET = {
    Arguments,
}

# Set of workflow phases.
PHASES = (
    phase_1,
    phase_2,
)


def parse_ctx(ctx: ExecutionContext):
    """Parse execution context prior to launching a run.
    
    """
    # Normally transfers are performed using an on-chain contract.
    # This generator overrides this default behaviour.
    ctx.use_client_contract_for_transfers = False
