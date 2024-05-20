from redis.asyncio.client import Redis


def get_redis_connection(host, port):
    return Redis(host=host, port=port)
