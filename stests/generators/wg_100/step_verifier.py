from stests.core.domain import RunContext
from stests.core.domain import RunStep
from stests.core.utils import logger
from stests.generators.wg_100 import step_verifier_phase_1 as phase_1_verifier



# Map: step name --> step verifier.
VERIFIERS = {
    "phase_1.do_fund_contract": phase_1_verifier.verify_do_fund_contract,
    "phase_1.do_fund_faucet": phase_1_verifier.verify_do_fund_faucet,
    "phase_1.do_fund_users": phase_1_verifier.verify_do_fund_users,
}


def verify(ctx: RunContext, deploy_hash: str) -> bool:
    """Verifies that a step has completed prior to incrementation.
    
    """
    try:
        verifier = VERIFIERS[ctx.run_step]
    except KeyError:
        logger.log_warning(f"{ctx.run_type} has no verifier for step {ctx.run_step}")
        return True
    else:
        return verifier(ctx, deploy_hash)
