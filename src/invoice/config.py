import os

DB_NAME='invoice'

def get_postgres_uri():
    host = os.environ.get('DB_HOST', 'localhost')
    port = 54321 if host == 'localhost' else 5432
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user, db_name = 'invoice', 'postgres'
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

def get_redis_host_and_port():
    host = os.environ.get('REDIS_HOST', 'localhost')
    port = 63791 if host == 'localhost' else 6379
    return dict(host=host, port=port)