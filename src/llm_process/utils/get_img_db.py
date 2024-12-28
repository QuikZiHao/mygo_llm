import psycopg2
from ..constants import LLM_CONFIG
from urllib.parse import urlparse


def get_image_db():
    connection_string = LLM_CONFIG["db_connection"]
    result = urlparse(connection_string)
    connection = psycopg2.connect(
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port,
        database=result.path[1:]  # Strip the leading '/' from the database name
    )
    return connection