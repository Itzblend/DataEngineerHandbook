from src.db.database import PostgresDatabase
import argparse
import sys
from enum import Enum


class MigrationOperation(Enum):
    MIGRATE = "migrate"
    REVERT = "revert"


def run(version: str, mode: str, dbname: str, host: str, print_only: bool):
    migration_file_path = f"src/migrations/{version}/{mode}.sql"

    try:
        migration_sql = open(migration_file_path).read()
    except FileNotFoundError:
        print(f"No migration file for {migration_file_path}")
        return

    print(f"==== Executing migration for {migration_file_path} ====")
    if print_only:
        print(migration_sql)
    else:
        db = PostgresDatabase(dbname=dbname, host=host)
        db.execute(migration_sql)
    print(f"==== Finished migration for {migration_file_path} ====")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--dbname", type=str)
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--version", type=str)
    parser.add_argument("--mode",
                        type=str,
                        choices=["migrate", "revert"],
                        default="migrate")
    parser.add_argument("--print-only", action="store_true")

    args, _ = parser.parse_known_args()

    if not args.version:
        print("Provide a version to run the script")
        sys.exit()

    run(args.version, args.mode, args.dbname, args.host, args.print_only)
