0.  Review repo

    - Open browser @ https://github.com/CasperLabs/stests
    - https://github.com/CasperLabs/stests/blob/master/installer

1.  Terminal 1

    ```stests-workers-interactive```

2.  Terminal 2 - start monitoring

    ```stests-monitoring-start```

3.  Terminal 2 - run a generator

    ```stests-wg-100 lrt1 --user-accounts 5 --run 1```

4.  Terminal 2 - list progress of all runs

    ```stests-ls-runs lrt1```

5.  Terminal 2 - list progress of a run

    ```stests-ls-run lrt1 wg-100 1```
