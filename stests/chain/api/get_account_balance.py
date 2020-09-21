from stests.core.types.infra import Node
from stests.core.types.infra import Network



def execute(
    network: Network,
    node: Node,
    account_id: str,
    block_hash: str = None,
    ) -> int:
    """Queries account balance at a certain block height | hash.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param account_id: Identifier of account whose balance will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account balance.

    """
    raise NotImplementedError("get-account-balance")
