def execute(
    block_hash: str,
    key: str,
    key_type: str,
    path: str,
    ) -> dict:
    """Queries node for an item within global state.

    :param block_hash: Hash of block at which point state query will be emitted.
    :param key: Name of key against which to issue a query.
    :param key_type: Type of key being queried.
    :param path: Path within global state data.

    :returns: Global state info pulled from chain.

    """     
    raise NotImplementedError("get-state")
