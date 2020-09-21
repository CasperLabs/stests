from stests.core import mq
from stests.core import logging
from stests.core.mq import encoder
from stests.core.types.logging import OutputMode



def setup_daemon():
    """Perform setup when run in daemon mode.
    
    """
    _setup(OutputMode.DAEMON)


def setup_interactive():
    """Perform setup when run in interactive mode.
    
    """
    _setup(OutputMode.INTERACTIVE)


def _setup(output_mode: OutputMode):
    """Perform setup tasks standard to all workers.
    
    """
    # Initialise logging.
    logging.initialise(output_mode)

    # Initialise broker.
    mq.initialise()

    # Initialise encoder.
    encoder.initialise()    


def start_orchestration():
    """Starts workload generators.
    
    """
    # JIT import actors: generators.
    import stests.orchestration.generators.wg_100.meta
    import stests.orchestration.generators.wg_110.meta

    # JIT import actors: orchestration.
    import stests.orchestration.engine.run
    import stests.orchestration.engine.phase
    import stests.orchestration.engine.step


def start_monitoring():
    """Starts chain monitoring.
    
    """
    # JIT import actors: monitoring.
    import stests.monitoring.control
    import stests.monitoring.listener

    # Start monitoring.
    from stests.monitoring.control import do_start_monitoring
    do_start_monitoring.send()
