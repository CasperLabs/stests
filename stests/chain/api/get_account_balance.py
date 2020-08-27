def execute(
    account_id: str,
    block_hash: str = None,
    ) -> int:
    """Queries account balance at a certain block height | hash.

    :param account_id: Identifier of account whose balance will be queried.
    :param block_hash: Hash of block against which query will be made.

    :returns: Account balance.

    """
    raise NotImplementedError("get-account-balance")
