import streamlit as st
from typing import Dict
from config_redis import azure_redis
import redis
import pickle


def redis_check():
    print("hellow from redis functions")


def _get_session_from_redis_cache(sid) -> Dict:
    """Retrieve session from Redis using the decoded session id, sid."""
    try:
        r: redis.StrictRedis = azure_redis
        key_prefix = "session:"
        val = r.get(key_prefix + sid)
        data: Dict = pickle.loads(val)
        return data

    except Exception as e:
        print(f"Error getting session from redis cache. {e}")
        return None


def get_data(key) -> Dict:
    try:
        print(f"getting data for key={key}")
        r: redis.StrictRedis = azure_redis
        key_prefix = "riddle:"
        val = r.get(key_prefix + key)
        if val:
            return val.decode("utf-8")
        return val

    except Exception as e:
        print(f"Error getting session from redis cache. {e}")
        return None


def set_data(key, value) -> Dict:
    try:
        r: redis.StrictRedis = azure_redis
        key_prefix = "riddle:"
        r.set(key_prefix + key, value)
        return None

    except Exception as e:
        print(f"Error getting session from redis cache. {e}")
        return None


def ping():
    r: redis.StrictRedis = azure_redis
    result = r.ping()
    return result
