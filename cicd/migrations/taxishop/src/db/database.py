import psycopg2
from contextlib import contextmanager


class PostgresDatabase:

    def __init__(self,
                 dbname: str,
                 host: str = "localhost",
                 port: int = 5432,
                 user: str = "postgres",
                 password: str = "postgres"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection_string = (
            f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        )

    @contextmanager
    def cursor(self):
        conn = psycopg2.connect(self.connection_string)
        conn.autocommit = False

        try:
            cursor = conn.cursor()
            yield cursor
        except psycopg2.Error:
            print("Error in db operation")
            raise
        finally:
            conn.commit()
            conn.close()
