import pandas as pd

from sqlalchemy import create_engine

from tqdm.auto import tqdm

import click


# Configuration

year = 2021

month = 1


# Data types

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}


parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


# Click configuration

@click.command()

@click.option('--pg-user', default='root')

@click.option('--pg-pass', default='root')

@click.option('--pg-host', default='localhost')

@click.option('--pg-port', default=5433, type=int)

@click.option('--pg-db', default='my_taxi')

@click.option('--target-table', default='yellow_taxi_data')


def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):


    # URL

    url = (
        f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
        f"yellow/yellow_tripdata_{year}-{month:02d}.csv.gz"
    )


    # PostgreSQL connection

    engine = create_engine(
        f"postgresql+psycopg://{pg_user}:{pg_pass}@"
        f"{pg_host}:{pg_port}/{pg_db}"
    )


    # Read data in chunks

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )


    # Create table once, then insert chunks

    first = True

    for df_chunk in tqdm(df_iter):

        if first:

            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists="replace"
            )

            first = False

            print("Table created")


        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))


if __name__ == '__main__':
    run()