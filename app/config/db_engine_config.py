# POOL_PRE_PING enables a "pre-ping" feature, sending a lightweight query to
# the database before each connection use, ensuring connection viability.
# This helps in preventing errors from idle database connections being dropped.
POOL_PRE_PING = True

# POOL_RECYCLE sets the maximum lifetime of database connections in seconds.
# Connections are recycled (closed and reopened) after this period.
# Here, set to 3600 seconds (1 hour) to prevent auto-closing by the DB.
POOL_RECYCLE = 3600

# KEEPALIVES settings configure TCP keepalive parameters, keeping the
# connection active in environments with firewalls/load balancers that
# may terminate idle connections.
# KEEPALIVES (1 to enable) activates TCP keepalive.
KEEPALIVES = 1

# KEEPALIVES_IDLE is the idle time in seconds before TCP starts sending
# keepalive probes. Set to 30 seconds.
KEEPALIVES_IDLE = 30

# KEEPALIVES_INTERVAL is the interval in seconds between keepalive probes.
# Set to 10 seconds.
KEEPALIVES_INTERVAL = 10

# KEEPALIVES_COUNT is the max number of keepalive probes before the
# connection is dropped. Set to 5.
KEEPALIVES_COUNT = 5
