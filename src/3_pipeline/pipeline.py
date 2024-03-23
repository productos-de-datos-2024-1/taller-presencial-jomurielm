"""ETL for importing house prices data from csv file to database"""

import glob
import json
import logging
import os.path
import shutil
import sqlite3

import pandas as pd
import pkg_resources

CONFIG_FILE = "config.json"


if not pkg_resources.resource_exists(__name__, CONFIG_FILE):
    raise FileNotFoundError(f"File {CONFIG_FILE} not found")

with pkg_resources.resource_stream(__name__, CONFIG_FILE) as f:
    config = json.load(f)

logging.basicConfig(
    filename=os.path.join(config["logs_dir"], config["pipeline_log"]),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def extract(cofig):
    """Extracts data from csv file"""

    logging.info("Starting data extraction")
    #
    path = os.path.join(cofig["stagging_dir"], "*.csv.zip")
    filenames = glob.glob(path)
    dataframes = [pd.read_csv(f, compression="zip") for f in filenames]
    df = pd.concat(dataframes)
    #
    logging.info("Data extraction completed")
    #
    return df


def transform(df):
    """Transforms data to be ready for loading"""

    logging.info("Starting data transformation")
    #
    df["date"] = pd.to_datetime(df["date"])
    #
    logging.info("Data transformation completed")
    #
    return df


def load(df):
    """Loads data to database"""

    logging.info("Starting data loading")
    #
    database = os.path.join(config["database_dir"], config["database_name"])
    conn = sqlite3.connect(database)
    df.to_sql("house_prices", conn, if_exists="append", index=False)
    conn.close()
    #
    logging.info("Data loading completed")


def etl():
    """Orchestrates ETL process"""

    logging.info("Starting ETL process")
    #
    df = extract(config)
    df = transform(df)
    load(df)
    #
    logging.info("ETL process completed")


def move_files():
    """Moves files from stagging to ingested folder"""

    logging.info("Starting file moving")
    #
    stagging_path = os.path.join(config["stagging_dir"], "*.csv.zip")
    ingested_dir = config["ingested_dir"]
    for source in glob.glob(stagging_path):
        target = os.path.join(ingested_dir, os.path.basename(source))
        shutil.move(source, target)
    #
    logging.info("File moving completed")


def downsampling():
    """Downsamples the database"""

    logging.info("Starting downsampling")
    #
    database = os.path.join(config["database_dir"], config["database_name"])
    conn = sqlite3.connect(database)
    df = pd.read_sql_query("SELECT * FROM house_prices", conn)
    conn.close()
    #
    sample = df.sample(frac=0.2, random_state=0)
    #
    train_sample = sample.sample(frac=0.8, random_state=0)
    train_file = os.path.join(config["downsampled_dir"], config["train_dataset"])
    train_sample.to_csv(train_file, index=False, compression="zip")
    logging.info("Train file created")
    #
    test_sample = sample.drop(train_sample.index)
    test_file = os.path.join(config["downsampled_dir"], config["test_dataset"])
    test_sample.to_csv(test_file, index=False, compression="zip")
    logging.info("Test file created")
    #


if __name__ == "__main__":
    etl()
    move_files()
    downsampling()