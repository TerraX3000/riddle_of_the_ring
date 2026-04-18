import redis

azure_redis = redis.StrictRedis(host="localhost", port=6379, decode_responses=False)
