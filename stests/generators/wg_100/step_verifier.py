from stests.core.domain import RunContext
from stests.core.domain import RunStep



def verify(ctx: RunContext, step: RunStep) -> bool:
    print(f"666 :: wg-100 :: verifier")
    return True
