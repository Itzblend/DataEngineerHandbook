from src.db.database import PostgresDatabase


db = PostgresDatabase("taxi")

with db.cursor() as cur:
    cur.execute("select 42;")
    print(cur.fetchone())
