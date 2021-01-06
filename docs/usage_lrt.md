# STESTS Usage For LRT

Within a Casper Labs LRT setting it is assumed that each LRT is associated with a **dedicated** stests box.  This document details pocess of setting up such such a box.  

## Step 0: Install stests library

### Pre-requisites

- [git](https://www.atlassian.com/git/tutorials/install-git)
- [python3](https://www.python.org/downloads) (3.8+)
- [pipenv](https://pipenv.kennethreitz.org/en/latest/install/#installing-pipenv)

### Installation

Once pre-requisites are in place then stests can be installed via the [installer](../installer):

```
curl https://raw.githubusercontent.com/CasperLabs/stests/master/installer | bash
```

The side effects of running the installer are as follows:

- stests repo cloned to:
	- `$HOME/casperlabs/stests`

- stests [default environment variables file](../resources/stests_vars.sh) copied to:
	- `$HOME/.casperlabs-stests/vars`

- stests [default supervisord config file](../resources/supervisord.conf) copied to:
	- `$HOME/.casperlabs-stests/ops/config`

- `$HOME/bashrc` file updated so as to activate stests [commands](commands.md) within terminal sessions. 

- stests python virtual environment crerated using pipenv.

Once the installer has run you must review the installed stests environment variable settings (i.e. `vi $HOME/.casperlabs-stests/vars`).

## Registering LRT Network Assets

Prior to interacting with a test network one must register various network assets infrastructure with stests, i.e. registering the network itself plus it's associated set of nodes.  Relevant private keys must also registered in order to support faucet and/or Proof-of-Stake scenarios.

To streamline registration stests provides the `stests-register-lrt` command.  This command assumes that network assets have already been copied to the `$HOME/.casperlabs-stests/nets/lrtX` folder as follows:

```
chainspec.toml
accounts.csv
nodes.csv
bin/casper-client
bin/*.wasm
configs/{NODE-IP}/secret_key.pem
faucet/secret_key.pem
```

NOTE - the contents of nodes.csv includes each node's HTTP server ip address & port.

Once the network assets are in place then simply run the `stests-register-lrt` command.  This will reset the stests infrastructure cache and [process the assets accordingly](../sh/scripts/cache_register_lrt.py).

## Post Registration

Testing session workflows will typically be as follow:

```
# Restart workers - ensures non-infra cache has been reset.
stests-workers-restart

# Run wasm-less transfers.
stests-wg-100 \
	--net lrtX \
	--transfers 1000 \
	--deploys-per-second 0.01

# Run wasm based transfers (wasm file per transfer).
stests-wg-110 \
	--net lrtX \
	--transfers 1000 \
	--deploys-per-second 0.01

# Observe network behaviour via node status endpoints, logs ...etc.
```

## ELK integration

The stests library emits various [events](../stests/events.py#L11-L63) of interest, some of which are related to the internal dynamics of stests itself, whilst others are related to chain activity.  The stests logging events are emitted as JSON blobs & are comsumable by logstash.  To instruct stests to push logs to logstash you can edit the `STESTS_LOGGING_LOGSTASH` prefixed stests environment variables file (see `$HOME/.casperlabs-stests/vars`).  This assumes that you have corectly setup the local logstash daemon.
