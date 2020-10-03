stests
===============

Casper Labs System Test Platform


What is stests ?
--------------------------------------

stests stands for system tests.  It's goal is to encapsulate large system testing of the CSPR network.


Why stests ?
--------------------------------------

Launching a blockchain network within a hostile permission-less setting is non-trivial.  The elevated risk profile of such an undertaking must be matched by a concomitant level of sophistication in respect of system testing.  At the core of such testing will be a test platform, i.e. stests, whose underlying strategic objective is to progressively constrain network behaviour to that of a successful production setting, i.e. main net.


Who uses stests ?
--------------------------------------

CSPR network community.  This encompasses developers, validators, evaluators ... etc.

Requirements
--------------------------------------

    - python 3.7+
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
    stests-cache-set-network poc1
    stests-cache-set-network-faucet-key poc1 path-to-faucet-private-key-pem-file
    ```

2.  Register nodes + node bonding keys:

    ```
    stests-cache-set-node poc1:1 {host}:{port} full
    stests-cache-set-node-bonding-key poc1:1 path-to-validator-private-key-pem-file

    stests-cache-set-node poc1:2 {host}:{port} full
    stests-cache-set-node-bonding-key poc1:2 path-to-validator-private-key-pem-file

    stests-cache-set-node poc1:3 {host}:{port} full
    stests-cache-set-node-bonding-key poc1:3 path-to-validator-private-key-pem-file
    ```

3.  Run a generator:

    ```
    # Run once.
    stests-wg-100 poc1 --user-accounts 5
    stests-wg-100 poc1 --user-accounts 50
    stests-wg-100 poc1 --user-accounts 500

    # Run 2 in parallel.
    stests-wg-100 poc1 --user-accounts 5 --parallel 2
    
    # Run 2 in parallel, each looping 4 times or until a failure occurs.
    stests-wg-100 poc1 --user-accounts 5 --parallel 2 --loop 4

    # Run 2 in parallel, each looping 4 times every 10 minutes.
    stests-wg-100 poc1 --user-accounts 5 --parallel 2 --loop 4 --loop-interval 600 --execution-mode periodic
    ```

Further Information ?
--------------------------------------

Please refer to the [specification](https://github.com/CasperLabs/stests/wiki/STESTS-Specification) for further information.
