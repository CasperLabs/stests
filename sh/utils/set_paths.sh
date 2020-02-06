# Root paths.
export STESTS_PATH_ROOT=$HOME/.casperlabs-stests
export STESTS_PATH_VARS=$STESTS_PATH_ROOT/vars
export STESTS_PATH_OPS=$STESTS_PATH_ROOT/ops

# Repo internal paths.
export STESTS_PATH_SH=$STESTS_HOME/sh
export STESTS_PATH_SRC=$STESTS_HOME/stests
export STESTS_PATH_CLI=$STESTS_HOME/stests/cli
export STESTS_PATH_GENERATORS=$STESTS_HOME/stests/generators
export STESTS_PATH_RESOURCES=$STESTS_HOME/resources
export STESTS_PATH_TEMPLATES=$STESTS_HOME/resources/templates

# Ensure shell scripts are executable.
chmod a+x $STESTS_PATH_SH/*.sh

# Ensure ops directories exist
mkdir -p $STESTS_PATH_OPS
mkdir -p $STESTS_PATH_OPS/config
mkdir -p $STESTS_PATH_OPS/daemon
mkdir -p $STESTS_PATH_OPS/logs
