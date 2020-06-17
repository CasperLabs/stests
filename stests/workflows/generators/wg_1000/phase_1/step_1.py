import json
import requests

from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionContext



# Step label.
LABEL = "increment-deploys"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Set target URL by selecting a node at random.
    node = cache.infra.get_node_by_network_nodeset(
        factory.create_network_id(ctx.network),
        ctx.node_index
        )
    url = f"http://{node.address}/deploys"

    # Set current count.
    deploy_count = len(json.loads(requests.get(url).content))
    
    # Cache current count for verification in phase 2.
    cache.workflow.set_deploy_count(ctx, deploy_count)

    # Build a 'deploy batch'.
    new_deploys = list(range(deploy_count + 1, deploy_count + 1 + ctx.args['deploys']))    

    # Push deploy batch to node.
    requests.post(url, json.dumps(new_deploys))
