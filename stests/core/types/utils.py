import enum
from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json
from dataclasses_json import config
from datetime import datetime

from marshmallow import fields



def get_isodatetime_field():
    """Returns an ISO datetime field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    """
    return field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


@dataclass_json
@dataclass
class Entity:
    """Base class for all entities flowing through system.
    
    """    
    @staticmethod
    def instantiate(typeof):
        """Factory: returns an instance for testing purposes.
        
        """
        try:
            typeof.create
        except AttributeError:
            return typeof()
        else:
            return typeof.create()

