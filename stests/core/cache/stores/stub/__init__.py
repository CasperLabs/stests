import fakeredis



def get_store(network_id: str) -> fakeredis.FakeStrictRedis:
    """Returns instance of a stubbed cache store.

    :param network_id: Network identifier, e.g. DEV-LOC-01
    :returns: An instance of a stubbed cache store.

    """
    return fakeredis.FakeStrictRedis()
