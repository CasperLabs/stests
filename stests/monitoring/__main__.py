import sys
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from stests.core import mq



# Initialise MQ sub-package.
mq.initialise()

# Import monitoring.
import stests.monitoring.chain
import stests.monitoring.correlator

# Import WG-100.
import stests.generators.wg_100.args
import stests.generators.wg_100.phase_1
import stests.generators.wg_100.phase_2

# Import monitoring launcher.
from stests.monitoring.chain import launch_stream_monitors
launch_stream_monitors.send()
