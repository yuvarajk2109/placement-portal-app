import logging
from extensions import redis_client
from flask import request
import json

logger = logging.getLogger(__name__)

DEFAULT_TTL = 600

def cache_response(ttl = DEFAULT_TTL, key_prefix = None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if redis_client is None:
                return 
            prefix = key_prefix or fn.__name__
            cache_key = f"cache:{prefix}:{request.full_path}"
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    logger.debug("Cache HIT:", cache_key)
                    return json.loads(cached), 200
            except Exception as e:
                logger.warning("Redis READ ERROR", e)
            result = fn(*args, **kwargs)
            if isinstance(result, tuple):
                response_data, status_code = result
                if status_code == 200:
                    try:
                        redis_client.setex(cache_key, ttl, json.dumps(response_data))
                        logger.debug(f"Cache SET: {cache_key}, TTL = {ttl}s")
                    except Exception as e:
                        logger.warning("Redis WRITE ERROR:", e)
                return response_data, status_code
            return result
        return wrapper
    return decorator

def invalidate_cache(pattern):
    if redis_client is None:
        return
    try:
        keys = redis_client.keys(f"cache:{pattern}:*")
        if keys:
            redis_client.delete(*keys)
            logger.info(f"Cache INVALIDATED: {len(keys)} keys matching '{pattern}")
    except Exception as e:
        logger.warning("Redis INVALIDATION ERROR:", e)