from stests.generators.wg_100 import phase_1
from stests.generators.wg_100 import phase_2



# Actor pipeline.
PIPELINE = (
    phase_1.do_init_cache,
    phase_1.do_create_accounts,
    phase_1.do_fund_faucet,
    phase_1.do_fund_contract,
    phase_1.do_fund_users,
    phase_2.do_deploy_contract,
    phase_2.do_start_auction,
)

# Map: actor --> verifier.
VERIFIERS = {
    phase_1.do_fund_contract: phase_1.verify_fund_contract,
    phase_1.do_fund_faucet: phase_1.verify_fund_faucet,
    phase_1.do_fund_users: phase_1.verify_fund_users,
}
