1. Test Platform Specification

    - open
    - navigate to section: NETWORK types
    - navigate to workload generators: WG-100

2. Redis Desktop Manager

    - open UI
    - show null db
    - briefly talk about state, 16 databases & keyspace

3. RabbitMQ Broker

    - open UI
    - show null broker 
    - create 2 vhosts + set permissions: 
        - LOC-DEV-01
        - INT-DEV-01
    - show empty queues

4. New shell: workflow phase 01

    cd $CLABS_HOME/stests
    pipenv shell
    python ./stests/generators/wg_100/phase_01/workflow.py --max-user-accounts=5

5. RabbitMQ broker 

    - open UI
    - show created queues
    - show sample messages

6. New shell: worker phase 01

    cd $CLABS_HOME/stests
    pipenv shell
    cd stests/
    dramatiq -p 1 -t 1 worker --path ~/Engineering/clabs/stests --watch ~/Engineering/clabs/stests/stests

7. RabbitMQ broker 

    - open UI
    - show empty queues

8. Redis Desktop Manager  

    - open UI
    - show cache contents

9. dramatiq

    - open web page @ https://dramatiq.io
    - briefly discuss features
        - daemonisation
        - decorators
        - sync / async modes
        - message time limits
        - dead queues, expiration queues
        - message retries
        - --watch flag
        - idempotence

10. Code design

    - core
        - cache
        - clx
        - mq
        types
    - generators
        - wg_100
    - utils
