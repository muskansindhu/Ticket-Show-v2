from flask import current_app as app
from flask_caching import Cache

app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/3'
app.config['CACHE_DEFAULT_TIMEOUT'] = 10
app.config['CACHE_TYPE'] = 'redis'
cache = Cache(app)
