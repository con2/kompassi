import redis
from kombu.transport import redis as kombu_redis


class HealthCheckingConnection(redis.Connection):
    # kombu passes health_check_interval only if it finds the parameter with inspect.getfullargspec.
    # redis-py 8 decorates AbstractConnection.__init__, which hides its parameters from getfullargspec,
    # so without this explicit parameter kombu silently drops the option and idle pub/sub connections
    # get closed by the haproxy in front of Redis.
    def __init__(self, *args, health_check_interval: int = 0, **kwargs):
        super().__init__(*args, health_check_interval=health_check_interval, **kwargs)


class Channel(kombu_redis.Channel):
    connection_class = HealthCheckingConnection


class Transport(kombu_redis.Transport):
    Channel = Channel
