# STESTS Usage

Once installed stests commands can be used to interact with the target test network.  Whilst there are many supported commands, a few subsets typically form the vast majority of user workflows.  

## Registering Infrastructure

Prior to interacting with a test network one must register the network infrastructure with stests, this includes registering the network itself plus it's associated set of nodes.  Relevant private keys are also registered in order to support faucet and/or Proof-of-Stake scenarios.

1.  Register network + faucet key:

    ```
    stests-set-network poc1
    stests-set-network-faucet-key poc1 path-to-faucet-private-key-pem-file
    ```

2.  Register nodes + node bonding keys:

    ```
    stests-set-node poc1:1 {host}:{port} full
    stests-set-node-bonding-key poc1:1 path-to-validator-private-key-pem-file

    stests-set-node poc1:2 {host}:{port} full
    stests-set-node-bonding-key poc1:2 path-to-validator-private-key-pem-file

    stests-set-node poc1:3 {host}:{port} full
    stests-set-node-bonding-key poc1:3 path-to-validator-private-key-pem-file
    ```

## Launching Workers

Once the network is registered you can launch stests monitoring & orchestration worker processes.  These processes run in daemon mode, i.e. in the background, and are controlled from the command line.

1.  Start workers.

	```
	stests-workers
	```

2.  From time to time it is a good idea to restart the workers so that the stests cache resources can be reset.

	```
	stests-workers-restart
	```

3.  Worker status can be viewed as follows:

	```
	stests-workers-status
	```

4.  Stop workers.

	```
	stests-workers-stop
	```

## Launching Workload Generators

Once the network is registered and workers are up & running, you can proceed to run workload generators.  Each generator is numbered and can be executed as follows:

- `stests-wg-XXX YYY` 
- XXX = generator ID
- YYY = network-ID

Whilst each workload generator is associated with it's own set of parameters, each generator is also associated with a default set of parameters:

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
