stests
===============

Casper Labs System Test Platform


What is stests ?
--------------------------------------

stests stands for system tests.  It's goal is to encapsulate very large system testing of the CLX network.


Why stests ?
--------------------------------------

Launching a blockchain network within a hostile permission-less setting is non-trivial.  The elevated risk profile of such an undertaking must be matched by a concomitant level of sophistication in respect of system testing.  At the core of such testing will be a test platform, i.e. stests, whose underlying strategic objective is to progressively constrain network behaviour to that of a successful production setting, i.e. main net.


Who uses stests ?
--------------------------------------

CLS network developer & DevOps community.


Installation
--------

```
curl https://raw.githubusercontent.com/CasperLabs/stests/master/installer | bash
```

Usage
--------

1.  Register network + faucet key:

    ```
    stests-set-network xxxy
    stests-set-network-faucet-key xxxy path-to-faucet-private-key-pem-file
    ```

2.  Register nodes + node bonding keys:

    ```
    stests-set-node xxxy:1 host:port full
    stests-set-node-bonding-key xxxy:1 path-to-validator-private-key-pem-file

    stests-set-node xxxy:1 host:port full
    stests-set-node-bonding-key xxxy:2 path-to-validator-private-key-pem-file

    stests-set-node xxxy:1 host:port full
    stests-set-node-bonding-key xxxy:3 path-to-validator-private-key-pem-file
    ```

3.  Start a generator:

    ```
    stests-wg-100 xxxy --run 1 --user-accounts 50
    ```

Further Information ?
--------------------------------------

Please refer to the [specification](https://casperlabs.atlassian.net/wiki/spaces/TEST/pages/156827909/Test+Platform+Specification) for further information.
