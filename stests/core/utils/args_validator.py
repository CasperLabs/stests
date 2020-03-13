import argparse

from stests.core.domain import NetworkType



# Network index min/max.
NETWORK_INDEX_MIN = 1
NETWORK_INDEX_MAX = 99

# Node index min/max.
NODE_INDEX_MIN = 1
NODE_INDEX_MAX = 999

# Port min/max.
PORT_MIN = 1
PORT_MAX = 65536

# Run index min/max.
RUN_INDEX_MIN = 1
RUN_INDEX_MAX = 65536

# Loop interval (in seconds) min/max
LOOP_INTERVAL_MIN = 0
LOOP_INTERVAL_MAX = 1209600  # 2 weeks

# Loop count min/max
LOOP_COUNT_MIN = -1
LOOP_COUNT_MAX = 65536


def validate_run_index(value):
    """Argument verifier: generator run index.
    
    """
    return _validate_int(value, RUN_INDEX_MIN, RUN_INDEX_MAX, "Generator")


def validate_run_type(value):
    """Argument verifier: generator run type.
    
    """
    # TODO
    return str(value).upper()


def validate_loop_interval(value):
    """Argument verifier: loop interval.
    
    """
    return _validate_int(value, LOOP_INTERVAL_MIN, LOOP_INTERVAL_MAX, "Loop interval")


def validate_loop_count(value):
    """Argument verifier: loop count.
    
    """
    return _validate_int(value, LOOP_COUNT_MIN, LOOP_COUNT_MAX, "Loop count")


def validate_network_index(value):
    """Argument verifier: network index.
    
    """
    return _validate_int(value, NETWORK_INDEX_MIN, NETWORK_INDEX_MAX, "Network")


def validate_network(value):
    """Argument verifier: network name.
    
    """
    name = str(value)

    # Validate network type.
    network_types = [i for i in NetworkType if name.startswith(i.name.lower())]
    if not network_types:
        raise argparse.ArgumentError("Invalid network name")

    # Validate network index.
    validate_network_index(name[len(network_types[0].name):])

    return name


def validate_node_address(value):
    """Argument verifier: node address.
    
    """
    address = str(value)
    parts = address.split(":")
    if len(parts) != 2:
        raise argparse.ArgumentError("Invalid node address")
    _validate_host(parts[0])
    _validate_port(parts[1])

    return address


def validate_node_index(value):
    """Argument verifier: node index.
    
    """
    return _validate_int(value, NODE_INDEX_MIN, NODE_INDEX_MAX, "Node")


def validate_node_name(value):
    """Argument verifier: node name.
    
    """
    name = str(value)
    parts = name.split(":")
    if len(parts) != 2:
        raise argparse.ArgumentError("Invalid node name")
    validate_network(name.split(":")[0])
    validate_node_index(name.split(":")[1])

    return name


def _validate_host(value):
    """Argument verifier: host.
    
    """
    # TODO: validate against a regex or 3rd party lib.
    pass


def _validate_port(value):
    """Argument verifier: port.
    
    """
    return _validate_int(value, PORT_MIN, PORT_MAX, "Port")


def _validate_enum(value, enum_type, type):
    """Validates a constrained integer value.
    
    """
    try:
        enum_type[value]
    except KeyError:
        err = f"expected {' | '.join([i.name.lower() for i in enum_type])}"
        raise argparse.ArgumentTypeError(err)


def _validate_int(value, min, max, type):
    """Validates a constrained integer value.
    
    """
    try:
        ivalue = int(value)
        if min and max:
            if ivalue < min or ivalue > max:
                raise ValueError()
    except ValueError:
        err = f"{type} index must be an integer"
        if min and max:
            err += f" between {min} and {max}"
        raise argparse.ArgumentTypeError(err)
        
    return ivalue
