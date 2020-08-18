# STESTS - Workload Generators

## Overview

The stests application can be used to dispatch various workloads to a target network.  Such workloads test scenarios pertaining to accounts, smart-contracts, and/or network infrastructure.    Workloads are executed from the command line according to the following command template:

- `stests-wg-XXX YYY` 
- XXX = generator ID
- YYY = network-ID

## Default Parameters

- `--deploys-per-second`
	- Max. number of deploys to dispatch per second.
    - Defaults to zero, i.e. dispatch as many as possible

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
	- Number of runs to launch in parallel.

## WG-004 - Node Deactivate / Activate

Disconnects or reconnects a node from/to a network.  Does this by executing RunDeck API within underlying SRE infrastructure.

## WG-000 - Temporary node-rs test generator

Launches a workload generator that queries a node's `deploys` endpoint to get a count of pseudo-deploys dispatched to network.  It then dipatches N pseudo-deploys, waits for 2 seconds, and then asserts that the new deploy count is as expected.

- `--deploys`
    Number of pseudo-deploys to dispatch.


## WG-100 - Balance Transfer (WASM-less)

Launches a workload generator that will perform a sequence of wasm-less on-chain balance transfers.  

- `--user-accounts`
    Number of user accounts to dynamically generate & use for transfer simulations.

- `--faucet-initial-clx-balance`
    - Initial CLX balance of run faucet account.

- `--contract-initial-clx-balance`
    - Initial CLX balance of contract account.

- `--user-initial-clx-balance`
    - Initial CLX balance of user accounts.
