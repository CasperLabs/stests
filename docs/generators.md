# STESTS - Workload Generators

## Overview

The stests tool is used to dispatch workloads to a target test network.  Workloads test scenarios realted to accounts, smart-contracts, and/or network infrastructure.  Workloads are executed from the command line according to the following command template:

- `stests-wg-X --net Y` 

- X = generator ID, Y = network-ID, e.g. nctl1

## Default Parameters

Depending upon the type of generator being executed the following set of **default** parameters are defineable:

- `--deploys-per-second`
	- Max. number of deploys to dispatch per second.

- `--execution-mode`
	- Generator execution mode - sequential | periodical
	- If a generator is launched in sequential mode AND is instructed to loop N times, then run N+1 will only be launched if run N successfully completed.
	- If a generator is launched in periodical mode AND is instructed to loop N times, then run N+1 will be scheduled for launch when run N starts.  Thus even if run N fails, run N+1 will be started.

- `--key-algorithm`
	- Elliptic Curve Cryptography algorithm used when creating accounts.

- `--loop`
	- Number of times to loop when running the generator multiple times.

- `--loop-interval`
	- Interval in seconds between loops.

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--node`
	- Node index - must be between 1 and 999. If specified deploys are dispatched to this node only, otherwise deploys are dispatched to random nodes.

- `--parallel`
	- Number of runs to launch in parallel.


## WG-100 - Transfer (native)

- `stests-wg-100 --net X --transfers Y --amount Z` 

Launches a workload generator that will perform a sequence of **native** balance transfers.  Also see default parameters above.

- `--net`
	- Network name {type}{id}, e.g. nctl1.
	
- `--transfers`
	- Number of transfers to dispatch. Default=100.

- `--amount`
	- Motes per transfer. Default=100000000.


## WG-101 - Transfer (native)

- `stests-wg-101 --net X --transfers Y --amount Z` 

Launches a workload generator that performs a sequence of native transfers in a fire & forget fashion - i.e. immediate dispatch with no monitoring.  

- `--net`
	- Network name {type}{id}, e.g. nctl1.
	
- `--transfers`
	- Number of transfers to dispatch. Default=100.

- `--amount`
	- Motes per transfer. Default=100000000.


## WG-110 - Balance Transfer (WASM based)

- `stests-wg-110 --net X --transfers Y --amount Z` 

Launches a workload generator that will perform a sequence of wasm-less on-chain balance transfers.  For each transfer **a WASM file will be dispatched** to the network as part of the deploy. 

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--transfers`
	- Number of transfers to dispatch. Default=100.

- `--amount`
	- Motes per transfer. Default=100000000.


## WG-111 - Fire & Forget Transfer (WASM based)

- `stests-wg-111 --net X --transfers Y --amount Z` 

Launches a workload generator that performs a sequence of wasm transfers in a fire & forget fashion - i.e. immediate dispatch with no monitoring.  For each transfer **a WASM file will be dispatched** to the network as part of the deploy. 

- `--net`
	- Network name {type}{id}, e.g. nctl1.

- `--transfers`
	- Number of transfers to dispatch. Default=100.

- `--amount`
	- Motes per transfer. Default=100000000.
