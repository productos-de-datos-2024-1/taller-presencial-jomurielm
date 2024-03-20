"""Autograding script"""

import os

# test code files
assert os.path.exists("src/4_model/config.json")
assert os.path.exists("src/4_model/train.py")

# test run
assert os.path.exists("datalake/models/house_prices_model.pkl")
