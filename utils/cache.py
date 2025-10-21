import hashlib
import json
import logging

def create_cache_key(*args, **kwargs) -> str:
    """
    Create a unique cache key from arguments.
    
    Args:
        *args: Positional arguments to include in cache key
        **kwargs: Keyword arguments to include in cache key
    
    Returns:
        str: MD5 hash of the serialized arguments
    """
    key_args = json.dumps(args, sort_keys=True, default=str)
    key_kwargs = json.dumps(kwargs, sort_keys=True, default=str)
    key_string = f"{key_args}:{key_kwargs}"
    return hashlib.md5(key_string.encode()).hexdigest()

def deserialize_cache_data(cached_data: str | dict | None) -> dict | None:
    """
    Deserialize cached data from dcc.Store (JSON string to dict).
    
    Args:
        cached_data: Data from dcc.Store (could be dict or JSON string)
    
    Returns:
        dict or None: Deserialized data or None if invalid
    """
    if not cached_data:
        return None
    
    if isinstance(cached_data, dict):
        return cached_data
    
    if isinstance(cached_data, str):
        try:
            return json.loads(cached_data)
        except json.JSONDecodeError:
            logging.warning("Failed to deserialize cached data")
            return None
    
    return None
