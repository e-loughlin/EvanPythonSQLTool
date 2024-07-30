import sqlite3
from abc import ABC, abstractmethod

import ibis
import pandas as pd


class DBHandler(ABC):
    """Abstract base class for handling database operations. Can be used to extend for other DB types"""

    @abstractmethod
    def get_table_sizes(self):
        pass

    @abstractmethod
    def get_row_counts(self):
        pass


# TODO: Write IbisDBHandler...


class SQLiteDBHandler(DBHandler):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def get_table_sizes(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_sizes = {}
        cursor.execute("PRAGMA page_size;")
        page_size = cursor.fetchone()[0]
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA page_count('{table_name}');")
            page_count = cursor.fetchone()[0]
            table_sizes[table_name] = (page_count * page_size) / (
                1024**2
            )  # Convert bytes to MB
        return table_sizes

    def get_row_counts(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        row_counts = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_counts[table_name] = cursor.fetchone()[0]
        return row_counts
