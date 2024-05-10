import os


def get_postgres_dsn() -> str:

    engine = os.environ.get("POSTGRES_ENGINE")
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    host = os.environ.get("POSTGRES_HOST")
    port = os.environ.get("POSTGRES_PORT")
    db_name = os.environ.get("POSTGRES_DB")

    dsn = f"{engine}://{user}:{password}@{host}:{port}/{db_name}"
    return dsn
