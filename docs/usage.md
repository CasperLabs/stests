# STESTS Usage

Once installed stests commands can be used to interact with the target test network.  Whilst there are many supported commands, a few subsets typically form the vast majority of user workflows.  

## Registering Infrastructure

Prior to interacting with a test network one must register the network infrastructure with stests, this includes registering the network itself plus it's associated set of nodes.  Relevant private keys are also registered in order to support faucet and/or Proof-of-Stake scenarios.

1.  Register network + faucet key:

    ```
    stests-cache-set-network --net poc1 --chain cspr-poc-chain
    stests-cache-set-faucet-key --net poc1 --path PATH_TO_SECRET_KEY
    ```

2.  Register nodes + node bonding keys:

    ```
    stests-cache-set-node --net poc1 --node 1 --address {host}:{port} --type full
    stests-cache-set-bonding-key --net poc1 --node 1 --path PATH_TO_SECRET_KEY

    stests-cache-set-node --net poc1 --node 2 --address {host}:{port} --type full
    stests-cache-set-bonding-key --net poc1 --node 2 --path PATH_TO_SECRET_KEY

    stests-cache-set-node --net poc1 --node 3 --address {host}:{port} --type full
    stests-cache-set-bonding-key --net poc1 --node 3 --path PATH_TO_SECRET_KEY
    ```

## Launching Workers

Once the network is registered you can launch stests monitoring & orchestration worker processes.  These processes run in daemon mode, i.e. in the background, and are controlled from the command line.  Prior to launching the workers ensure that the casper-node client binary + client side wasm files have been copied to a directory made availabel via the `CSPR_BIN` environment variable.

1.  Start workers.

	```
	stests-workers
	```

2.  From time to time it is a good idea to restart the workers so that stests cache resources can be reset.

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

Workload generator commands are documented [here](generators.md).
