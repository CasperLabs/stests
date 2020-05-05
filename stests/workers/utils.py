from stests.core import logging
from stests.core import mq
from stests.core.mq import encoder



def setup_daemon():
    """Perform setup when run in daemon mode.
    
    """
    _setup(logging.OutputMode.DAEMON)


def setup_interactive():
    """Perform setup when run in interactive mode.
    
    """
    _setup(logging.OutputMode.INTERACTIVE)


def _setup(output_mode: logging.OutputMode):
    """Perform setup tasks standard to all workers.
    
    """
    # Initialise logging.
    logging.initialise(output_mode)

    # Initialise broker.
    mq.initialise()

    # Initialise encoder.
    encoder.initialise()    


def start_workflows():
    """Starts workload generators.
    
    """
    # JIT import actors: generators.
    import stests.workflows.generators.wg_100.meta
    import stests.workflows.generators.wg_110.meta
    import stests.workflows.generators.wg_200.meta
    import stests.workflows.generators.wg_210.meta

    # JIT import actors: orchestration.
    import stests.workflows.orchestration.run
    import stests.workflows.orchestration.phase
    import stests.workflows.orchestration.step


def start_monitoring():
    """Starts chain monitoring.
    
    """
    # JIT import actors: monitoring.
    import stests.monitoring.control
    import stests.monitoring.listener

    # Start monitoring.
    from stests.monitoring.control import do_start_monitoring
    do_start_monitoring.send()