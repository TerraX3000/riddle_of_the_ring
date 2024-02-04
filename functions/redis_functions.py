import streamlit as st
from typing import Dict
from config_redis import azure_redis
import redis
import pickle
from icecream import ic


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


def get_data(key, game_code=None) -> Dict:
    try:
        print(f"getting data for key={key}")
        r: redis.StrictRedis = azure_redis
        key_prefix = "riddle:"
        if game_code:
            key_prefix += f"{game_code}:"
        val = r.get(key_prefix + key)
        if val:
            return val.decode("utf-8")
        return val

    except Exception as e:
        print(f"Error getting data from redis cache. {e}")
        return None


def set_data(key, value, game_code=None) -> Dict:
    try:
        r: redis.StrictRedis = azure_redis
        key_prefix = "riddle:"
        if game_code:
            key_prefix += f"{game_code}:"
        r.set(key_prefix + key, value)
        return None

    except Exception as e:
        print(f"Error setting data in redis cache. {e}")
        return None


def data_exists(key, game_code=None) -> bool:
    try:
        r: redis.StrictRedis = azure_redis
        key_prefix = "riddle:"
        if game_code:
            key_prefix += f"{game_code}:"
        does_exist = r.exists(key_prefix + key)
        return does_exist
    except Exception as e:
        print(f"Error checking if data exists in redis cache. {e}")
        return None


def delete_data(key, game_code=None):
    try:
        r: redis.StrictRedis = azure_redis
        key_prefix = "riddle:"
        if game_code:
            key_prefix += f"{game_code}:"
        r.delete(key_prefix + key)
    except Exception as e:
        print(f"Error deleting from redis cache. {e}")
        return None


def ping():
    r: redis.StrictRedis = azure_redis
    result = r.ping()
    return result
