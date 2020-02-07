from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.types.enums import AccountType
from stests.core.types.identifiers import AccountIdentifier
from stests.core.types.identifiers import GeneratorRunIdentifier
from stests.core.types.identifiers import NetworkIdentifier
from stests.core.types.identifiers import NodeIdentifier
from stests.core.utils import defaults



@dataclass_json
@dataclass
class GeneratorRun:
    """Information associated with each generator run.
    
    """
    # Associated network reference information.
    network: NetworkIdentifier

    # Associated node reference information.
    node: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator being executed.
    typeof: str


    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return self.get_identifier().cache_key


    def get_account_identifier(self, index: int, typeof: AccountType) -> AccountIdentifier:
        """Returns an identifier pertaining to an account.
        
        """
        return AccountIdentifier(
            self.get_identifier(),
            index,
            self.get_network_identifier(),
            typeof
        )


    def get_network_identifier(self) -> NetworkIdentifier:
        """Returns an identifier pertaining to the network.
        
        """
        # TODO: simplify domain model and then implement this.
        return self.network


    def get_node_identifier(self):
        """Returns an identifier pertaining to the node.
        
        """
        return NodeIdentifier(
            self.get_network_identifier(),
            self.node
            )


    def get_identifier(self) -> GeneratorRunIdentifier:
        """Returns an identifier pertaining to the generator.
        
        """
        return GeneratorRunIdentifier(
            self.get_network_identifier(),
            self.run,
            self.typeof
        )


    @classmethod
    def create(
        cls,
        network=defaults.NETWORK_NAME,
        node=defaults.NODE_INDEX,
        run=defaults.GENERATOR_RUN,
        typeof="WG-XXX"
        ):
        """Factory method: leveraged in both live & test settings.
        
        """
        return cls(NetworkIdentifier.create(network), node, run, typeof)


@dataclass_json
@dataclass
class GeneratorRunStatus:
    """Generator workflow status - as distinct from execution status.
    
    """
    # Associated generator run information.
    run: GeneratorRunIdentifier

    # New status.
    status: str

    # Moment in time when status change occurred.
    timestamp: int

    @property
    def cache_key(self):
        """Returns key to be used when caching an instance."""
        return f"{self.run.cache_key}:events:{self.timestamp}"
