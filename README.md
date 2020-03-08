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

CLX network community.  This encompasses developers, validators, evaluators ... etc.


Requirements
--------------------------------------

    - python 3.7+
    - redis

Installation
--------------------------------------

```
curl https://raw.githubusercontent.com/CasperLabs/stests/master/installer | bash
```

Usage
--------------------------------------

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

3.  Run a generator:

    ```
    stests-wg-100 poc1 --run 1 --user-accounts 5
    stests-wg-100 poc1 --run 2 --user-accounts 50
    stests-wg-100 poc1 --run 3 --user-accounts 500
    ```

Further Information ?
--------------------------------------

Please refer to the [specification](https://casperlabs.atlassian.net/wiki/spaces/TEST/pages/156827909/Test+Platform+Specification) for further information.