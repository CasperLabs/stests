0. Pre-Demo

    ```
    rm -rf $CLABS_OPS
    mkdir -p $CLABS_OPS
    delete MQ vhost
    flush cache
    ```

1. Test Platform Specification

    - open
    - navigate to section: NETWORK types
    - navigate to workload generators: WG-100

2. Redis Desktop Manager

    - open UI
    - show null db

3. Rabbit MQ Broker

    - open UI
    - show null broker 
    - create vhost: 
        - DEV-LOC-01
    - set vhost permission -> clabs-mq-stests-user
    - show empty queues

4.  Initialise chain resources: DEV-LOC-01

    ```
    printenv | grep CLABS | sort
    ls $CLABS_OPS

    cl-stests-init-chain-resources DEV-LOC-01

    ls $CLABS_OPS/chains
    ls $CLABS_OPS/chains/DEV-LOC-01
    ls $CLABS_OPS/chains/DEV-LOC-01/nodes

    vi $CLABS_OPS/chains/DEV-LOC-01/chainspec/genesis/csv/accounts.csv
    ```

5.  Cache chain info

    ```
    cl-stests-set-network --help
    cl-stests-set-network --network-id DEV-LOC-01 --lifetime SINGLETON --operator-type LOCAL
    ```

6.  Initialise node resources

    ```
    cl-stests-init-node-resources DEV-LOC-01 001

    ls $CLABS_OPS/chains/DEV-LOC-01/nodes/node-001
    ls $CLABS_OPS/chains/DEV-LOC-01/nodes/node-001/certs
    ls $CLABS_OPS/chains/DEV-LOC-01/nodes/node-001/keys

    vi $CLABS_OPS/chains/DEV-LOC-01/chainspec/genesis/csv/accounts.csv        
    ```

7.  Cache node info

    ```
    cl-stests-set-node --help
    cl-stests-set-node --network-id DEV-LOC-01 --name NODE-001 --host localhost --port 40400 --typeof FULL
    ```

8.  Start execution engine (in new terminal)

    ```
    cl-stests-run-ee DEV-LOC-01 001
    ```

9.  Start execution engine (in new terminal)

    ```
    cl-stests-run-node-standalone DEV-LOC-01 001
    ```

10. New shell: workflow phase 01

    ```
    cd $CLABS_HOME/stests
    pipenv shell
    python ./stests/generators/wg_100/phase_01/workflow --help
    python ./stests/generators/wg_100/phase_01/workflow --network-id DEV-LOC-01 --user-accounts=5
    ```

11. RabbitMQ broker 

    - open UI
    - show created queues
    - show sample messages

12. Existing shell: worker phase 01

    ```
    cd stests/generators/wg_100/phase_01
    export CL_STESTS_CONFIG_NETWORK_ID=DEV-LOC-01
    dramatiq -p 1 -t 1 worker --path $CLABS_HOME/stests --watch $CLABS_HOME/stests/stests
    ```

13. EE & NODE terminals

    - show logging output

14. RabbitMQ broker 

    - open UI
    - show empty queues

15. Redis Desktop Manager  

    - open UI
    - show cache contents

16. Code design

    - core
        - cache
        - clx
        - mq
        - types
    - generators
        - wg_100
    - scripts (cli)
