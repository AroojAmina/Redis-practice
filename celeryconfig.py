import os

# Redis Configuration
REDIS_URL = "redis://localhost:6379/0"

# Flask-Caching Configuration
CACHE_TYPE = "RedisCache"
CACHE_REDIS_URL = REDIS_URL

# Celery Configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
REDIS_URL = "redis://localhost:YOUR_PORT_NUMBER/0"
