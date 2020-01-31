# --------------------------------------------------------------------
# Cache
# --------------------------------------------------------------------

# type (REDIS | STUB)
export STESTS_CACHE_TYPE="REDIS"

# redis host
export STESTS_CACHE_REDIS_HOST="localhost"

# redis port
export STESTS_CACHE_REDIS_PORT=6379

# --------------------------------------------------------------------
# Message Broker
# --------------------------------------------------------------------

# type (REDIS | RABBIT | STUB)
export STESTS_BROKER_TYPE="REDIS"

# redis db #
export STESTS_BROKER_REDIS_DB=0
# redis host
export STESTS_BROKER_REDIS_HOST=localhost
# redis port
export STESTS_BROKER_REDIS_PORT=5672

# rabbit host
export STESTS_BROKER_RABBIT_HOST=localhost
# rabbit port
export STESTS_BROKER_RABBIT_PORT=5672
# rabbit protocol
export STESTS_BROKER_RABBIT_PROTOCOL=amqp
# rabbit ssl client cert path
export STESTS_BROKER_RABBIT_SSL_CLIENT_CERT=
# rabbit ssl client cert key path
export STESTS_BROKER_RABBIT_SSL_CLIENT_KEY=
# rabbit user
export STESTS_BROKER_RABBIT_USER=stests-mq-user
# rabbit user password
export STESTS_BROKER_RABBIT_USER_PWD=clabs
