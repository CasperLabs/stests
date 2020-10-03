stests
===============

Casper Network System Test Platform


What is stests ?
--------------------------------------

The stests library is a CSPR network system testing tool.


Why stests ?
--------------------------------------

Launching a blockchain network within a hostile permission-less setting is non-trivial.  The elevated risk burden demands a multi-faceted and sophisticated approach in respect of system testing.  One pillar of such system testing is stests, a library desiged to support progressively constraining network behaviour to that of a successful production setting, i.e. main net.


Who uses stests ?
--------------------------------------

CSPR network community.  This encompasses developers, validators, evaluators ... etc.

Requirements
--------------------------------------

    - python 3.8+
    - pipenv
    - redis

Installation
--------------------------------------

See [installation](docs/installation.md) for further information.

```
curl https://raw.githubusercontent.com/CasperLabs/stests/master/installer | bash
```

Commands
--------------------------------------

Once installed a set of [commands](docs/commands.md) are available for use within a terminal session.

Usage
--------------------------------------

See [usage](docs/usage.md) for further information.

Quick Start
--------------------------------------

1.  Register network + faucet key:

    ```
    stests-cache-set-network --net poc1
    stests-cache-set-faucet-key --net poc1 --path path-to-faucet-private-key-pem-file
    ```

2.  Register nodes + node bonding keys:

    ```
    stests-cache-set-node --net poc1 --node 1 --address {host}:{port} --type full
    stests-cache-set-bonding-key --net poc1 --node 1 --path path-to-validator-private-key-pem-file

    stests-cache-set-node --net poc1 --node 2 --address {host}:{port} --type full
    stests-cache-set-bonding-key --net poc1 --node 2 --path path-to-validator-private-key-pem-file

    stests-cache-set-node --net poc1 --node 3 --address {host}:{port} --type full
    stests-cache-set-bonding-key --net poc1 --node 3 --path path-to-validator-private-key-pem-file
    ```

3.  Run a generator:

    ```
    # Run once.
    stests-wg-100 --net poc1 --user-accounts 5
    stests-wg-100 --net poc1 --user-accounts 50
    stests-wg-100 --net poc1 --user-accounts 500

    # Run 2 in parallel.
    stests-wg-100 --net poc1 --user-accounts 5 --parallel 2
    
    # Run 2 in parallel, each looping 4 times or until a failure occurs.
    stests-wg-100 --net poc1 --user-accounts 5 --parallel 2 --loop 4

    # Run 2 in parallel, each looping 4 times every 10 minutes.
    stests-wg-100 --net poc1 --user-accounts 5 --parallel 2 --loop 4 --loop-interval 600 --execution-mode periodic
    ```

Further Information ?
--------------------------------------

Please refer to the [specification](https://github.com/CasperLabs/stests/wiki/STESTS-Specification) for further information.
