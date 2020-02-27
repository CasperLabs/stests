import typing
from dataclasses import dataclass

from stests.core.utils.domain import *



@dataclass
class RunContext(Entity):
    """Contextual information associated with each generator run.
    
    """
    # Associated run arguments.
    args: typing.Optional[typing.Any]

    # Associated network.
    network: str

    # Associated node index.
    node: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str

    # Current run step.
    run_step: typing.Optional[str]

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_isodatetime_field(True)

    # Timestamp: update.
    _ts_updated: datetime = get_isodatetime_field(True)

    # Universally unique identifier.
    _uid: str = get_uuid_field(True) 

    @property
    def run_index(self):
        return self.run
