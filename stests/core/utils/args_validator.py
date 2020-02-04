import argparse

from stests.core.types.enums import NetworkType



# Network index min/max.
NETWORK_IDX_MIN = 1
NETWORK_IDX_MAX = 99

# Node index min/max.
NODE_IDX_MIN = 1
NODE_IDX_MAX = 999

# Node port min/max.
NODE_PORT_MIN = 1
NODE_PORT_MAX = 65536

# Generarator run index min/max.
GENERATOR_RUN_IDX_MIN = 1
GENERATOR_RUN_IDX_MAX = 65536


def validate_network_idx(value):
    """Argument verifier: network index.
    
    """
    return validate_int(value, NETWORK_IDX_MIN, NETWORK_IDX_MAX, "Network")


def validate_network_name(value):
    """Argument verifier: network name.
    
    """
    # TODO: use reg-ex.
    name = str(value)
    try:
        validate_enum(name[:3].upper(), NetworkType, "Network")
    except argparse.ArgumentError:
        raise argparse.ArgumentError("Invalid network name: prefix shou")
    validate_int(name[3:], NETWORK_IDX_MIN, NETWORK_IDX_MAX, "Network")

    return name


def validate_node_index(value):
    """Argument verifier: node index.
    
    """
    return validate_int(value, NODE_IDX_MIN, NODE_IDX_MAX, "Node")


def validate_node_port(value):
    """Argument verifier: node port.
    
    """
    return validate_int(value, NODE_PORT_MIN, NODE_PORT_MAX, "Node Port")


def validate_generator_run_idx(value):
    """Argument verifier: generator run index.
    
    """
    return validate_int(value, GENERATOR_RUN_IDX_MIN, GENERATOR_RUN_IDX_MAX, "Generator")


def validate_enum(value, enum_type, typeof):
    """Validates a constrained integer value.
    
    """
    try:
        enum_type[value]
    except KeyError:
        err = f"expected {' | '.join([i.name for i in enum_type])}"
        raise argparse.ArgumentTypeError(err)


def validate_int(value, min, max, typeof):
    """Validates a constrained integer value.
    
    """
    try:
        ivalue = int(value)
        if min and max:
            if ivalue < min or ivalue > max:
                raise ValueError()
    except ValueError:
        err = f"{typeof} index must be an integer"
        if min and max:
            err += f" between {min} and {max}"
        raise argparse.ArgumentTypeError(err)
        
    return ivalue
