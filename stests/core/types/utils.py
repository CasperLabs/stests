import uuid
from dataclasses import field
from dataclasses_json import config
from datetime import datetime

from marshmallow import fields



def get_isodatetime_field(set_default=False):
    """Returns an ISO datetime field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    """
    if set_default == True:
        return field(
            default_factory=datetime.now,
            metadata=config(
                encoder=datetime.isoformat,
                decoder=datetime.fromisoformat,
                mm_field=fields.DateTime(format='iso')
            )
        )
    return field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


def get_uuid_field(set_default=False):
    """Returns a UUID4 field.
    
    :param default_factory: Factory method when underlying field value is initialised.

    """
    if set_default == True:
        return field(
            default_factory=lambda: str(uuid.uuid4()),
        )
    return field()
