import dataclasses
import datetime
import enum
import inspect
import json
import typing
import typing_inspect

from stests.core.utils import logger



# Set: supported enum values.  
ENUM_TYPE_SET = set()

# Map: enum keys -> enums.  
ENUM_VALUE_MAP = dict()

# Map: dataclass typekey -> dataclass type.  
DCLASS_MAP = dict()

# Set: supported dataclass types.  
DCLASS_SET = set()

# Set: primitive data types.
PRIMITIVES = (type(None), int, str, float, bool)


def as_dict(data: typing.Any) -> typing.Any:
    """Encodes input data in readiness for downstream processing.
    
    """
    return encode(data)


def as_json(data: typing.Any) -> str:
    """Encodes input data as JSON.
    
    """
    return json.dumps(encode(data), indent=4).encode("utf-8")


def from_dict(obj: typing.Any) -> typing.Any:
    """Encodes input data in readiness for downstream processing.
    
    """
    return decode(obj)


def from_json(as_json: str) -> typing.Any:
    """Encodes input data as JSON.
    
    """
    return decode(json.loads(as_json))


def decode(obj: typing.Any) -> typing.Any:
    """Decodes previously encoded information.
    
    """
    if isinstance(obj, PRIMITIVES):
        return obj

    if isinstance(obj, tuple):
        return tuple(map(decode, obj))

    if isinstance(obj, list):
        return list(map(decode, obj))

    if isinstance(obj, dict) and '_type_key' in obj:
        return _decode_dclass(obj)

    if isinstance(obj, dict):
        return {k: decode(v) for k, v in obj.items()}        

    if isinstance(obj, str) and obj in ENUM_VALUE_MAP:
        return ENUM_VALUE_MAP[obj]

    return obj


def _decode_dclass(obj):
    """Decodes a registered data class instance.
    
    """
    # Set data class type.
    dcls = DCLASS_MAP[obj['_type_key']]

    # Convert fields:
    for field in dataclasses.fields(dcls):
        if field.name not in obj:
            continue

        field_value = obj[field.name]
        if isinstance(field_value, type(None)):
            continue 

        field_type = _get_field_type(field)
        if field_type is datetime.datetime:
            obj[field.name] = datetime.datetime.fromtimestamp(field_value)

        elif field.type in ENUM_TYPE_SET:
            obj[field.name] = field.type[obj[field.name]]
    
        elif field_type in DCLASS_SET:
            obj[field.name] = _decode_dclass(obj[field.name])

        else:
            obj[field.name] = decode(obj[field.name])

    return dcls(**obj)


def _get_field_type(field):
    """Returns a dataclass field type.
    
    """
    # For optional fields the dataclass type annotation Union needs to be deconstruacture.
    if typing_inspect.get_origin(field.type) is typing.Union:
        type_args = typing_inspect.get_args(field.type)
        for type_arg in [i for i in type_args if i not in (type(None), )]:
            return type_arg
    else:
        return field.type


def encode(data: typing.Any) -> typing.Any:
    """Encodes input data in readiness for downstream processing.
    
    """
    if isinstance(data, PRIMITIVES):
        return data

    if isinstance(data, datetime.datetime):
        return data.timestamp()

    if isinstance(data, dict):
        return {k: encode(v) for k, v in data.items()}

    if isinstance(data, tuple):
        return tuple(map(encode, data))

    if isinstance(data, list):
        return list(map(encode, data))

    if type(data) in DCLASS_SET:
        return _encode_dclass(data, dataclasses.asdict(data))

    if type(data) in ENUM_TYPE_SET:
        return data.name

    logger.log_warning(f"Encoding an unrecognized data type: {data}")

    return data


def _encode_dclass(data, obj):
    """Encodes a data class that has been previously registered with the encoder.
    
    """
    # Inject typekey for subsequent roundtrip.
    obj['_type_key'] = f"{data.__module__}.{data.__class__.__name__}"

    # Recurse through properties that are also registered data classes.
    for i in [i for i in dir(data) if i in obj and not i.startswith('_') and 
                                      type(getattr(data, i)) in DCLASS_SET]:
        _encode_dclass(getattr(data, i), obj[i])

    return encode(obj)


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
