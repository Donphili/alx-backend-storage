#!/usr/bin/env python3
"""A python script that interacts with redis database"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
'''The module-level Redis instance.
'''

def data_cacher(method: Callable) -> Callable:
    @wraps(method)
    def invoker(url) -> str:
        # Increment count
        redis_store.incr(f'count:{url}', 1)
        
        # Get and increment count
        count = redis_store.get(f'count:{url}').decode('utf-8')
        
        result = redis_store.get(f'result:{url}')
        
        if result:
            return result.decode('utf-8')
        
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        
        return count  # Return the count value after increment

    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
