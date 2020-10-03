# STESTS Commands

## Overview

Upon successful installation a set of stests commands are available for execution from within a terminal session.  All such commands are prefixed by `stests-`, support the `--help` flag, and allow you to perform tasks:

- updating stack;
- controlling worker daemons;
- controlling interactive sessions;
- cache querying;
- cache updating;
- cache housekeeping;
- launching workload generators;
- viewing on-chain information;

## Updating Stack

#### `stests-stack-view-vars`

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

#### `stests-cache-view-contracts --net XXX`

Displays information related to all smart contracts registered with stests & stored on-chain.

#### `stests-cache-view-networks`

Displays information related to the set of networks registered with stests.

#### `stests-cache-view-network-faucet-key --net XXX`

Displays a network's faucet account ECC key pair.

#### `stests-cache-view-nodes`

Displays set of nodes registered with stests for a particular network.

#### `stests-cache-view-node-bonding-key`

Displays a node's bonding ECC key pair.

#### `stests-cache-view-run`

Displays summary information related to a workload generator run.  The information is broken down into the various phases/steps that a generator may pass through in it's lifetime.

#### `stests-cache-view-run-deploys`

Displays information about each deploy dispatched during the course of a workload generator run.

#### `stests-cache-view-runs`

Displays summary information regarding workload generator runs.  Such information includes number of dispatched deploys plus execution stats & status. 








## Cache Updating

#### `stests-set-contracts`

Registers various smart contracts used by workload generators.  Contracts are installed on-chain.

#### `stests-cache-set-network`

Registers a network for testing.

#### `stests-cache-set-network-faucet-key`

Registers a network's faucet key.

#### `stests-cache-set-network-status`

Updates the operational status of a registered network.

#### `stests-set-node`

Registers a network node.  When registering the node's mode must be specified as this will affect how stests will interact with the node.

#### `stests-set-node-bonding-key`

Registers a node's bonding key for use in Proof-of-Stake related scenarios.

#### `stests-set-node-status`

Updates the operational status of a registered node.

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

#### `stests-wg-004`

Disconnects or reconnects a node from/to a network.  Does this by executing RunDeck API within underlying SRE infrastructure.

#### `stests-wg-100`

Launches a workload generator that will perform a sequence of on-chain balance transfers.  For each transfer a WASM file will be dispatched to the network as part of the deploy.

#### `stests-wg-110`

Launches a workload generator that will perform a sequence of on-chain balance transfers.  For each transfer an on-chain WASM contract is referenced via it's hash.

## Viewing On-Chain Information

On-chain information can be queried, the query result is formatted and is displayed in the user's terminal session.  Binary information such as public keys, block hashes ...etc, are displayed in hexadecimal format.

#### `stests-view-balance`

Displays an account's on-chain balance or zero if the chain does not exist.

#### `stests-view-block-info`

Display information pertaining to a block.

#### `stests-view-deploy-info`

Display information pertaining to a deploy.

##### `stests-view-faucet-balance`

Displays a network's faucet account balance.
