"""Funciones comunes de input/"""

import os.path
from config import DATABASE_DIR, DATABASE_NAME


def get_database_path():
    """Returns the database path"""
    return os.path.join(DATABASE_DIR, DATABASE_NAME)
