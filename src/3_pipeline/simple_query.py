"""Simple query for testing purposes"""

import json
import os.path
import sqlite3

import pkg_resources

CONFIG_FILE = "config.json"

if not pkg_resources.resource_exists(__name__, CONFIG_FILE):
    raise FileNotFoundError(f"File {CONFIG_FILE} not found")

with pkg_resources.resource_stream(__name__, CONFIG_FILE) as f:
    config = json.load(f)


def simple_query():
    """Simple query for testing purposes"""

    query = "SELECT * FROM house_prices LIMIT 5"
    database = os.path.join(config["database_dir"], config["database_name"])
    conn = sqlite3.connect(database)
    result = conn.execute(query).fetchall()
    conn.close()
    for t in result:
        print(t)


if __name__ == "__main__":
    simple_query()