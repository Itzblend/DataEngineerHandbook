import faker
import sys
import psycopg2
from datetime import timedelta
import random
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("taxi-data-generator")

payment_columns = [
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "congestion_surcharge",
    "airport_fee",
]


def generate_taxi_data(interval):
    fake = faker.Faker()
    while True:
        start_time = fake.past_datetime(start_date="-1h")
        trip_duration_minutes = fake.random_int(min=5, max=60)
        end_time = start_time + timedelta(minutes=trip_duration_minutes)
        new_row = {
            "VendorID": random.randint(1, 2),
            "tpep_pickup_datetime": str(start_time),
            "tpep_dropoff_datetime": str(end_time),
            "passenger_count": fake.random_int(min=1, max=4),
            "trip_distance": random.uniform(0.1, 10.0),
            "RatecodeID": fake.random_int(min=1, max=2),
            "store_and_fwd_flag": fake.random_int(min=1, max=2),
            "PULocationID": fake.random_int(min=1, max=200),
            "DOLocationID": fake.random_int(min=1, max=200),
            "payment_type": fake.random_int(min=1, max=2),
            "fare_amount": random.uniform(3.0, 100.0),
            "extra": random.uniform(0.5, 2.0),
            "mta_tax": random.uniform(0.5, 2.0),
            "tip_amount": random.uniform(0.5, 2.0),
            "tolls_amount": random.uniform(0.5, 2.0),
            "improvement_surcharge": random.uniform(0.5, 2.0),
            "congestion_surcharge": random.uniform(0.5, 2.0),
            "airport_fee": random.uniform(0.0, 2.0),
        }
        new_row["total_amount"] = sum(
            [new_row[col] for col in payment_columns]
        )
        insert_taxi_row(new_row)
        logger.info(
            f"Inserted 1 row to taxi_trips table. Sleeping for {interval} seconds..."
        )
        sleep(interval)


def insert_taxi_row(row):
    insert_query = """
    INSERT INTO taxi_trips (
        VendorID,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        RatecodeID,
        store_and_fwd_flag,
        PULocationID,
        DOLocationID,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        congestion_surcharge,
        total_amount,
        airport_fee
    ) VALUES (
        %(VendorID)s,
        %(tpep_pickup_datetime)s,
        %(tpep_dropoff_datetime)s,
        %(passenger_count)s,
        %(trip_distance)s,
        %(RatecodeID)s,
        %(store_and_fwd_flag)s,
        %(PULocationID)s,
        %(DOLocationID)s,
        %(payment_type)s,
        %(fare_amount)s,
        %(extra)s,
        %(mta_tax)s,
        %(tip_amount)s,
        %(tolls_amount)s,
        %(improvement_surcharge)s,
        %(congestion_surcharge)s,
        %(total_amount)s,
        %(airport_fee)s
    );
    """

    cursor.execute(insert_query, row)
    conn.commit()


if __name__ == "__main__":
    print("Usage: python datagen.py <interval>")
    if len(sys.argv) < 2:
        sys.exit(1)

    interval = int(sys.argv[1])

    try:
        conn = psycopg2.connect(
            dbname="taxi",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
        )
        cursor = conn.cursor()
        generate_taxi_data(interval=interval)
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)
