import json
import random
import requests
import sys

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionContext



# Step label.
LABEL = "increment-deploys"

# Max. size of a u32 integer in rust.
MAX_RUST_U32 = 4294967295


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    network_id = factory.create_network_id("lrt1")

    network = cache.infra.get_network(network_id)
    for node in cache.infra.get_nodes(network_id):
        if node.port == 50000:
            break

    account = node.account
    secret_key_pem_filepath = node.account.get_private_key_pem_filepath()

    # Set target URL by selecting a node at random.
    # node = cache.infra.get_node_by_network_nodeset(
    #     factory.create_network_id(ctx.network),
    #     ctx.node_index
    #     )

    deploy_hash = chain.put_deploy(
        account=account,
        network=network,
        node=node,
        contract_fname="transfer_to_account_u512.wasm",
    )


    # # Set current count.
    # deploy_count = len(json.loads(requests.get(url).content))
    
    # # Cache current count for verification in phase 2.
    # cache.workflow.set_deploy_count(ctx, deploy_count)

    # # Build a 'deploy batch' = list of random integers.
    # new_deploys = list(map(lambda _: random.randint(0, MAX_RUST_U32), range(ctx.args['deploys'])))

    # # Push deploy batch to node.
    # requests.post(url, json.dumps(new_deploys))

