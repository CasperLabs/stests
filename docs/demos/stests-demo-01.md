1. Redis Desktop Manager

    - open UI
    - show db

2. Rabbit MQ Broker

    - open UI
    - show vhost 

3.  Initialise chain & standalone node

    ```
    clabs-init-chain-resources lrt-01
    ls $CLABS_OPS/chains
    ls $CLABS_OPS/chains/lrt-01    

    clabs-init-node-resources lrt-01 001

    ls $CLABS_OPS/chains/lrt-01/nodes/node-001
    ls $CLABS_OPS/chains/lrt-01/nodes/node-001/certs
    ls $CLABS_OPS/chains/lrt-01/nodes/node-001/keys

    vi $CLABS_OPS/chains/lrt-01/chainspec/genesis/accounts.csv        
    ```

4.  Register network + node with stests

    ```
    stests-cache-set-network lrt1
    stests-cache-set-faucet-key lrt1 $CLABS_OPS/chains/lrt-01/nodes/node-001/keys/validator-private.pem
    stests-set-node lrt1:1 localhost:40401 full
    stests-set-node-bonding-key lrt1:1 $CLABS_OPS/chains/lrt-01/nodes/node-001/keys/validator-private.pem
    ```

5. Open Redis 

    - show network & node entries

6.  In terminal 1, start execution engine

    ```
    clabs-run-ee lrt-01 001
    ```

7.  In terminal 2, start node

    ```
    clabs-run-node-standalone lrt-01 001
    ```

8. In terminal 3, launch stests worker daemon

    ```
    stests-workers-run
    stests-workers-status
    ```

9. Open RabbitMQ 

    - show queues + consumers

10. In terminal 4, launch stests workload generator

    ```
    stests-wg-100 --help
    stests-wg-100 lrt1 --run 1 --user-accounts 5
    ```

11. EE & NODE terminals

    - show logging output

12. Open RabbitMQ 

    - show empty queues

13. Open Redis

    - show context, accounts, deploys, events entries

14. In terminal 4, launch stests workload generator

    ```
    stests-wg-100 lrt1 --run 2 --user-accounts 100
    stests-wg-100 lrt1 --run 3 --user-accounts 1000
    stests-wg-100 lrt1 --run 4 --user-accounts 10000
    ```
