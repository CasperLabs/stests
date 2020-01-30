import argparse


# Network index min/max.
NETWORK_IDX_MIN = 1
NETWORK_IDX_MAX = 99

# Node index min/max.
NODE_IDX_MIN = 1
NODE_IDX_MAX = 999



def validate_network_idx(value):
    """Argument verifier: network index.
    
    """
    return validate_idx(value, NETWORK_IDX_MIN, NETWORK_IDX_MAX, "Network")


def validate_node_idx(value):
    """Argument verifier: node index.
    
    """
    return validate_idx(value, NODE_IDX_MIN, NODE_IDX_MAX, "Node")


def validate_idx(value, min, max, typeof):
    """Argument verifier: index.
    
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
