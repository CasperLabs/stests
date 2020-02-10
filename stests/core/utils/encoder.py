import enum
import inspect
import typing



# Set: supported enum values.  
ENUM_TYPE_SET = set()

# Map: enum keys -> enums.  
ENUM_VALUE_MAP = dict()

# Map: dataclass typekey -> dataclass type.  
DCLASS_MAP = dict()

# Set: supported dataclass types.  
DCLASS_SET = set()


def decode(obj: typing.Any) -> typing.Any:
    """Decodes previously encoded information.
    
    """
    if isinstance(obj, tuple):
        return tuple(map(decode, obj))

    if isinstance(obj, list):
        return list(map(decode, obj))

    if isinstance(obj, dict) and 'meta' in obj and 'type_key' in obj['meta']:
        return _decode_registered_dclass(obj)

    if isinstance(obj, dict):
        return {k: decode(v) for k, v in obj.items()}        

    if isinstance(obj, str) and obj in ENUM_VALUE_MAP:
        return ENUM_VALUE_MAP[obj]

    return obj


def _decode_registered_dclass(obj):
    """Decodes a registered data class instance.
    
    """
    dclass_type = DCLASS_MAP[obj['meta']['type_key']]
    data = dclass_type.from_dict(obj)

    # Recursively ensure child domain model instances are also decoded.
    for k, v in obj.items():
        if isinstance(v, dict) and 'meta' in v and 'type_key' in v['meta']:
            setattr(data, k, _decode_registered_dclass(v))

    return data


def encode(data: typing.Any) -> typing.Any:
    """Encodes input data in readiness for downstream processing.
    
    """
    if isinstance(data, dict):
        return {k: encode(v) for k, v in data.items()}

    if isinstance(data, tuple):
        return tuple(map(encode, data))

    if isinstance(data, list):
        return list(map(encode, data))

    if type(data) in DCLASS_SET:
        return _encode_registered_dclass(data, data.to_dict())

    if type(data) in ENUM_TYPE_SET:
        return str(data)

    if str(data) in ENUM_VALUE_MAP:
        return str(data)

    return data


def _encode_registered_dclass(data, obj):
    """Encodes a data class that has been previously registered with the encoder.
    
    """
    # Inject typekey for subsequent roundtrip.
    obj['meta'] = obj.get('meta', {})
    obj['meta']['type_key'] = f"{data.__module__}.{data.__class__.__name__}"

    # Recurse through properties that are also registered data classes.
    for i in [i for i in dir(data) if not i.startswith('_') and 
                                      type(getattr(data, i)) in DCLASS_SET]:
        _encode_registered_dclass(getattr(data, i), obj[i])

    return obj


def register_type(cls):
    """Workflows need to extend the typeset so as to ensure that arguments are decoded/encoded correctly.
    
    """
    global ENUM_TYPE_SET
    global DCLASS_SET

    if issubclass(cls, (enum.Enum, enum.Flag)):
        ENUM_TYPE_SET = ENUM_TYPE_SET | {cls, }
        for i in cls:
            ENUM_VALUE_MAP[str(i)] = i
    else:
        DCLASS_MAP[f"{cls.__module__}.{cls.__name__}"] = cls
        DCLASS_SET = DCLASS_SET | { cls, }
