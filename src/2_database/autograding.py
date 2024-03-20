"""Autograding script"""

import os

# test code files
assert os.path.exists("src/2_database/config.json")
assert os.path.exists("src/2_database/create_database.py")
assert os.path.exists("src/2_database/create_table.sql")

# database
assert os.path.exists("datalake/databases/house_prices.db")
