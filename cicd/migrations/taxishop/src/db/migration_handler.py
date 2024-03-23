from src.db.database import PostgresDatabase
import argparse
import sys
from enum import Enum


class MigrationOperation(Enum):
    MIGRATE = "migrate"
    REVERT = "revert"


def run(version: str, mode: str, dbname: str):
    migration_file_path = f"src/migrations/{version}/{mode}.sql"
    migration_sql = open(migration_file_path).read()

    db = PostgresDatabase(dbname)
    db.execute(migration_sql)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--dbname", type=str)
    parser.add_argument("--version", type=str)
    parser.add_argument("--mode",
                        type=str,
                        choices=["migrate", "revert"],
                        default="migrate")

    args, _ = parser.parse_known_args()

    if not args.version:
        print("Provide a version to run the script")
        sys.exit()

    run(args.version, args.mode, args.dbname)