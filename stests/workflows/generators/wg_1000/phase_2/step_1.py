import json
import requests
import time

from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionContext



# Step label.
LABEL = "verify-deploys"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Grant baby network has time to propogate.
    time.sleep(2.0)

    # Set target URL by selecting a node at random.
    node = cache.infra.get_node_by_network_nodeset(
        factory.create_network_id(ctx.network),
        ctx.node_index
        )
    url = f"http://{node.address}/deploys"

    # Get deploy count just before posting deploy batch.
    count_cached = cache.workflow.get_deploy_count(ctx)['deploy_count']

    # Get  deploy count.
    count_actual = len(json.loads(requests.get(url).content))

    # Assert actual count is likely to be correct by comparing against cached count plus user defined increments. 
    assert count_actual >= count_cached + ctx.args['deploys'], "Deploy count mismatch"
