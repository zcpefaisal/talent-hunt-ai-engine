from slowapi import Limiter
from slowapi.util import get_remote_address

# Setting up the rate limiter with Redis as the storage backend
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://my_fastapi_app_redis:6379"
)