# STESTS Commands

## Overview

Upon successful installation a set of stests commands are available for execution from within a terminal session.  All such commands are prefixed by `stests-` and allow you to perform tasks:

- updating stack;
- controlling worker daemons;
- controlling interactive sessions;
- cache querying;
- cache updating;
- cache housekeeping;
- launching workload generators;
- viewing on-chain information;

Listed below are the full set of supported commands with the exception of workload generator commands which are documented [here](generators.md).

## Updating Stack

#### `stests-stack-vars`

Displays in terminal full set of sests environment variables.

#### `stests-stack-update`

Updates installed stests stack by:

- pulling latest changes from stests GitHub repo;
- updating environment variables;
- updating virtual environment.

## Controlling Worker Daemons

The stests worker processes can be run in daemon mode.  Process behaviour can be altered by editing the following configuration file:

- `$HOME/.casperlabs-stests/ops/config/supervisord.conf`

#### `stests-interactive`

Runs worker processes in a single interactive session.  Interactive mode is useful in development & smokescreen scenarios.

#### `stests-workers` | `stests-workers-start`

Starts stests worker processes in daemon mode.  

#### `stests-workers-reload`

Stops stests worker processes, pauses for 3 seconds, and then restarts processes.  **Does not flush cache**.  

#### `stests-workers-restart`

Stops stests worker processes, pauses for 3 seconds, **flushes cache**, and then restarts processes. 

#### `stests-workers-status`

Displays in terminal current status of stests processes.

#### `stests-workers-stop`

Stops all stests worker processes currently running in daemon mode.

## Cache Housekeeping

The stests cache is implemented using Redis.  It is partitioned into sub-caches: orchestration, monitoring & infrastructure.  The cache size grows in proportion to the amount of time a target network is monitored and the number of executed workload generators.  The following commands simplify cache housekeeping.   

#### `stests-cache-flush`

Deletes orchestration & monitoring related cache data.

#### `stests-cache-flush-infra`

Deletes infrastructure related cache data.  **Execution of this command requires subsequent re-registration of network infrastructure**.

## Cache Querying

#### `stests-cache-view-bonding-key --net X --node Y`

Displays a node's bonding asymmetric ECC key pair.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--node`
	- Node index, e.g. 1.

#### `stests-cache-view-contracts --net X`

Displays information related to test smart contracts registered with stests & stored on-chain.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

#### `stests-cache-view-faucet-key --net X`

Displays a network's faucet account ECC key pair.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

#### `stests-cache-view-networks`

Displays information related to the set of networks registered with stests.

#### `stests-cache-view-nodes`

Displays set of nodes registered with stests for a particular network.

#### `stests-cache-view-run --net X --type Y --run Z`

Displays summary information related to a workload generator run.  The information is broken down into the various phases/steps that a generator may pass through in it's lifetime.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--type`
	- Run type, e.g. wg-100.
	
- `--run`
	- Run identifier, e.g. 1.

#### `stests-cache-view-run-deploys --net X --type Y --run Z`

Displays information about each deploy dispatched during the course of a workload generator run.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--type`
	- Run type, e.g. wg-100.
	
- `--run`
	- Run identifier, e.g. 1.

#### `stests-cache-view-runs --net X --type Y --status Z`

Displays summary information regarding workload generator runs.  Such information includes number of dispatched deploys plus execution stats & status. 

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--type`
	- Run type, e.g. wg-100.
	
- `--status`
	- Run status - e.g. complete.  

## Cache Updating

#### `stests-cache-set-bonding-key --net X --node Y --path Z`

Registers a node's bonding key for use in Proof-of-Stake related scenarios.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--node`
	- Node index, e.g. 1.

- `--path`
	- Absolute path to the node's secret key in PEM format.

#### `stests-cache-set-faucet-key --net X --path Y`

Registers a network's faucet key.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--path`
	- Absolute path to the faucet secret key in PEM format.

#### `stests-cache-set-network --net X`

Registers a network for testing.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

#### `stests-cache-set-network-status --net X --status Y`

Updates operational status of a registered network.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--status`
	- Network status.

#### `stests-cache-set-node --net X --node Y --address Z --type ZZ`

Registers a network node.  When registering the node's mode must be specified as this will affect how stests will interact with the node.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--node`
	- Node index, e.g. 1.

- `--address`
	- Node public network address: {host}:{port}.

- `--type`
	- Node type, i.e. full | read_only.

#### `stests-cache-set-node-status --net X --node Y --staus Z`

Updates the operational status of a registered node.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--node`
	- Node index, e.g. 1.

- `--status`
	- Node status.
