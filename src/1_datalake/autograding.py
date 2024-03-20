"""Autograding script"""

import os

# test code files
assert os.path.exists("src/1_datalake/create_datalake.py")
assert os.path.exists("src/1_datalake/datalake_structure.txt")

# test datalake structure
assert os.path.exists("datalake/databases/")
assert os.path.exists("datalake/downsampled_data/")
assert os.path.exists("datalake/logs/")
assert os.path.exists("datalake/models/")
assert os.path.exists("datalake/raw/stagging/")
assert os.path.exists("datalake/raw/ingested/")
