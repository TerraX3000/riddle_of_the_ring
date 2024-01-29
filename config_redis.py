import redis
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, "local.env"))

redis_hostname = os.getenv("AZURE_REDIS_HOSTNAME")
redis_password = os.getenv("AZURE_REDIS_PASSWORD")
azure_redis = redis.StrictRedis(
    host=redis_hostname, port=6380, db=0, password=redis_password, ssl=True
)
print(azure_redis)
