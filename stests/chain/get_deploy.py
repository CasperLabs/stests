from stests.core.types.infra import Node



# Method upon client to be invoked.
_CLIENT_METHOD = "get-deploy"


def execute(node: Node, deploy_hash: str = None) -> str:
    """Queries a node for a deploy.

    :param node: Target node being tested.
    :param deploy_hash: Hash of deploy being pulled.

    :returns: Representation of a deploy within a node's state.

    """
    # Map inputs to pycspr objects.
    node_client = node.as_pycspr_client

    return node_client.queries.get_deploy(deploy_hash)
