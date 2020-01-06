from stests.core.mq.middleware.results import get_middleware as _get_mware_results


def get_middleware():
    """Returns middleware to be applied to a broker.
    
    """
    return (_get_mware_results(), )