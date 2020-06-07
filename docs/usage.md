# STESTS Usage

## Overview

Upon successful installation a set of stests commands are available for execution from within a terminal session.  All such commands are prefixed by `stests-` and allow you to perform tasks:

- updating stack;
- controlling worker daemons;
- controlling interactive sessions;
- managing cache;
- launching workload generator runs;
- viewing on-chain information;
- viewing workload generator run information;

### Updating Stack

#### `stests-stack-update`

Updates the locally installed stests stack by:

- pulling latest changes from stests GitHub repo;
- updating environment variables;
- updating virtual environment.

### Controlling Worker Daemons

#### `stests-workers` | `stests-workers-start`

Starts stests processes in daemon mode.  Process behaviour can be altered by editing the following configuration file:

- `$HOME/.casperlabs-stests/ops/config/supervisord.conf`

#### `stests-workers-reload`

Stops stests processes, pauses for 3 seconds, and then restarts processes.  **Does not flush cache**.  

#### `stests-workers-restart`

Stops stests processes, pauses for 3 seconds, flushes cache, and then restarts processes. 

#### `stests-workers-status`

Displays in terminal the current status of stests processes.

#### `stests-workers-stop`

Stops all stests processes currently running in daemon mode.

### Managing Cache

#### `stests-flush`

Deletes monitoring & generator related cache data.

#### `stests-flush-infra`

Deletes infrastructure related cache data.  Execution of this command requires subsequent re-registration of network infrastructure.

### Controlling Interactive Sessions

Running orchestration & monitoring processes in interactive mode is useful in development & smokescreen scenarios.

#### `stests-interactive`

Runs both monitoring & orchestration processes in a single interactive session.

#### `stests-interactive-monitoring`

Runs monitoring process in a single interactive session.  Useful when wishing to focus upon node monitoring events.

#### `stests-interactive-orchestration`

Runs orchestration process in a single interactive session.
