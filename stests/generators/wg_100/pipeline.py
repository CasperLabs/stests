from stests.generators.wg_100 import phase_1
from stests.generators.wg_100 import phase_2
from stests.generators.wg_100 import phase_3



# Actor pipeline.
PIPELINE = (
    # phase 1
    phase_1.do_init_cache,
    phase_1.do_create_accounts,
    phase_1.do_fund_faucet,
    phase_1.do_fund_contract,
    phase_1.do_fund_users,
    # phase 2
    phase_2.do_deploy_contract,
    phase_2.do_start_auction,
    # phase 3
    phase_3.do_refund_step_1,
    phase_3.do_refund_step_2,
    phase_3.do_notify_completion,
)

# Map: actor --> verifier.
VERIFIERS = {
    # phase 1
    phase_1.do_fund_contract: phase_1.verify_fund_contract,
    phase_1.do_fund_faucet: phase_1.verify_fund_faucet,
    phase_1.do_fund_users: phase_1.verify_fund_users,
    # phase 3
    phase_3.do_refund_step_1: phase_3.verify_refund_step_1,
    phase_3.do_refund_step_2: phase_3.verify_refund_step_2,
}
