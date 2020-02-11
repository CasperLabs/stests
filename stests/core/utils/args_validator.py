import argparse

from stests.core.domain import NetworkType



# Network index min/max.
NETWORK_IDX_MIN = 1
NETWORK_IDX_MAX = 99

# Node index min/max.
NODE_IDX_MIN = 1
NODE_IDX_MAX = 999

# Port min/max.
PORT_MIN = 1
PORT_MAX = 65536

# Generarator run index min/max.
GENERATOR_RUN_IDX_MIN = 1
GENERATOR_RUN_IDX_MAX = 65536


def validate_host(value):
    """Argument verifier: host.
    
    """
    # TODO: validate against a regex or 3rd party lib.
    pass


def validate_network_idx(value):
    """Argument verifier: network index.
    
    """
    return validate_int(value, NETWORK_IDX_MIN, NETWORK_IDX_MAX, "Network")


def validate_network_name(value):
    """Argument verifier: network name.
    
    """
    name = str(value)

    # Validate prefix.
    network_types = [i for i in NetworkType if name.startswith(i.name.lower())]
    if not network_types:
        raise argparse.ArgumentError("Invalid network name")

    # Validate suffix.
    network_type = network_types[0]
    network_index = name[len(network_type.name):]
    validate_int(network_index, NETWORK_IDX_MIN, NETWORK_IDX_MAX, "Network")

    return name


def validate_node_address(value):
    """Argument verifier: node address.
    
    """
    address = str(value)
    parts = address.split(":")
    if len(parts) != 2:
        raise argparse.ArgumentError("Invalid node address")
    validate_host(parts[0])
    validate_port(parts[1])

    return address


def validate_node_name(value):
    """Argument verifier: node name.
    
    """
    name = str(value)
    parts = name.split(":")
    if len(parts) != 2:
        raise argparse.ArgumentError("Invalid node name")
    validate_network_name(name.split(":")[0])
    validate_node_index(name.split(":")[1])

    return name


def validate_node_index(value):
    """Argument verifier: node index.
    
    """
    return validate_int(value, NODE_IDX_MIN, NODE_IDX_MAX, "Node")


def validate_port(value):
    """Argument verifier: port.
    
    """
    return validate_int(value, PORT_MIN, PORT_MAX, "Port")


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
        err = f"expected {' | '.join([i.name.lower() for i in enum_type])}"
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
