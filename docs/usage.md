# STESTS Usage

## Overview

Upon successful installation a set of stests commands are available for execution from within a terminal session.  All such commands are prefixed by `stests-` and allow you to perform tasks:

- updating stack;
- controlling worker daemons;
- controlling interactive sessions;
- managing cache;
- launching workload generators;
- viewing on-chain information;
- viewing workload generator information;

## Updating Stack

#### `stests-stack-update`

Updates the locally installed stests stack by:

- pulling latest changes from stests GitHub repo;
- updating environment variables;
- updating virtual environment.

## Controlling Worker Daemons

The stests worker processes can be run in daemon mode.  Process behaviour can be altered by editing the following configuration file:

- `$HOME/.casperlabs-stests/ops/config/supervisord.conf`

#### `stests-workers` | `stests-workers-start`

Starts stests processes in daemon mode.  

#### `stests-workers-reload`

Stops stests processes, pauses for 3 seconds, and then restarts processes.  **Does not flush cache**.  

#### `stests-workers-restart`

Stops stests processes, pauses for 3 seconds, flushes cache, and then restarts processes. 

#### `stests-workers-status`

Displays in terminal the current status of stests processes.

#### `stests-workers-stop`

Stops all stests processes currently running in daemon mode.

## Controlling Interactive Sessions

Running orchestration & monitoring processes in interactive mode is useful in development & smokescreen scenarios.

#### `stests-interactive`

Runs both monitoring & orchestration processes in a single interactive session.

#### `stests-interactive-monitoring`

Runs monitoring process in a single interactive session.  Useful when wishing to focus upon node monitoring events.

#### `stests-interactive-orchestration`

Runs orchestration process in a single interactive session.

## Managing Cache

The stests cache is implemented using Redis.  It is partitioned into 3 sub-caches: orchestration, monitoring & infrastructure.  The cache size will grow in proportion to the amount of time a target network is monitored and the number of worklopad generators that have been executed.

#### `stests-flush`

Deletes orchestration & monitoring related cache data.

#### `stests-flush-infra`

Deletes infrastructure related cache data.  Execution of this command requires subsequent re-registration of network infrastructure.

## Launching Workload Generators

The stests application can be used to dispatch various workloads to a target network.  Such workloads may test scenarios pertaining to accounts, smart-contracts, and/or network infrastructure.    Workloads are executed from the command line:

- `stests-wg-XXX YYY` 
- XXX = generator ID
- YYY = network-ID

For each workload generator a set of default parameters may be defined:

- `--deploys-per-second`
	- Max. number of deploys to dispatch per second.

- `--execution-mode`
	- Generator execution mode - sequential | periodical
	- If a generator is launched in sequential mode AND is instructed to loop N times, then run N+1 will only be launched if run N successfully completed.
	- If a generator is launched in periodical mode AND is instructed to loop N times, then run N+1 will be scheduled for launch when run N starts.  Thus even if run N fails, run N+1 will be started.

- `--node`
	- Node index - must be between 1 and 999. If specified deploys are dispatched to this node only, otherwise deploys are dispatched to random nodes.

- `--loop`
	- Number of times to loop when running the generator multiple times.

- `--loop-interval`
	- Interval in seconds between loops.

- `--parallel`
	- "Number of runs to launch in parallel.

## Viewing On-Chain Information

On-chain information can be queried, the query result is formatted and is displayed in the user's terminal session.  Binary information such as public keys, block hashes ...etc, are displayed in hexadecimal format.

#### `stests-view-balance`

Displays an account's on-chain balance or zero if the chain does not exist.

#### `stests-view-block-info`

Display information pertaining to a block.

#### `stests-view-deploy-info`

Display information pertaining to a deploy.

## Viewing Workload Generator Information

TODO
