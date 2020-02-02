from dramatiq.brokers.stub import StubBroker



# Factory simply instantiates an instance.
get_broker = StubBroker
