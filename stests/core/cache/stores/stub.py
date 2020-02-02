import fakeredis


# Factory simply instantiates an instance.
get_store = fakeredis.FakeStrictRedis
