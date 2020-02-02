# --------------------------------------------------------------------
# Cache
# --------------------------------------------------------------------

# type (REDIS | STUB)
export STESTS_CACHE_TYPE="REDIS"

# --------------------------------------------------------------------
# Cache: REDIS
# --------------------------------------------------------------------

# Cache -> REDIS -> db
export STESTS_CACHE_REDIS_DB=1

# Cache -> REDIS -> host
export STESTS_CACHE_REDIS_HOST="localhost"

# Cache -> REDIS -> port
export STESTS_CACHE_REDIS_PORT=6379

# --------------------------------------------------------------------
# Message Broker
# --------------------------------------------------------------------

# type (REDIS | RABBIT | STUB)
export STESTS_BROKER_TYPE="REDIS"

# --------------------------------------------------------------------
# Message Broker: REDIS
# --------------------------------------------------------------------

# Broker -> REDIS -> db #
export STESTS_BROKER_REDIS_DB=0

# Broker -> REDIS -> host
export STESTS_BROKER_REDIS_HOST=localhost

# Broker -> REDIS -> port
export STESTS_BROKER_REDIS_PORT=5672

# --------------------------------------------------------------------
# Message Broker: RABBIT
# --------------------------------------------------------------------

# Broker -> RABBIT -> host
export STESTS_BROKER_RABBIT_HOST=localhost

# Broker -> RABBIT -> port
export STESTS_BROKER_RABBIT_PORT=5672

# Broker -> RABBIT -> protocol
export STESTS_BROKER_RABBIT_PROTOCOL=amqp

# Broker -> RABBIT -> ssl client cert path
export STESTS_BROKER_RABBIT_SSL_CLIENT_CERT=

# Broker -> RABBIT -> ssl client cert key path
export STESTS_BROKER_RABBIT_SSL_CLIENT_KEY=

# Broker -> RABBIT -> user
export STESTS_BROKER_RABBIT_USER=stests-mq-user

# Broker -> RABBIT -> user password
export STESTS_BROKER_RABBIT_USER_PWD=clabs

# Broker -> RABBIT -> virtual host
export STESTS_BROKER_RABBIT_VHOST=CLABS
