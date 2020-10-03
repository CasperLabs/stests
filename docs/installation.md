# STESTS - Installation

## Pre-requisites

- python 3.8+
- pipenv
- redis

- N.B Redis is the default message broker, however RabbitMQ is also supported. 

## Stack Installer

The stests library is bundled with an installer which can be invoked in a single command:

```
curl https://raw.githubusercontent.com/CasperLabs/stests/master/installer | bash
```

The installer detects the user's OS and installs the following:

- GitHub repo:
	- installed -> `$HOME/casperlabs/stests`
	- contains source code + associated bash scripts

- environment variables:
	- installed -> `$HOME/.casperlabs-stests/vars`
	- permits user to override various stests settings 

- worker daemon config:
	- installed -> `$HOME/.casperlabs-stests/ops/config/supervisord.conf`
	- controls number of processes allocated to stests daemon processes

- shell activator:
	- appended to end of `$HOME/.bashrc` | `$HOME/.bash_profile` 
	- ensures that stests commands are available within terminal sessions

- virtual environment:
	- installed using pipenv (see pre-requisites)

## Stack Update

To update to the latest version of stests simply execute the `stests-stack-update` command from within a terminal session.  The updater does the following:

- GitHub repo:
	- pulls latests changes.

- environment variables:
	- backs up existing settings -> `$HOME/.casperlabs-stests/vars-YYYY-MM-DD` 
	- installs new settings -> `$HOME/.casperlabs-stests/vars` 

- virtual environment:
	- updates environment to use latest dependencies
