import sqlite3
import unittest
from unittest.mock import MagicMock

from binchicken.db_handler import SQLiteDBHandler


class TestSQLiteDBHandler(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock(sqlite3.Connection)
        self.cursor = MagicMock(sqlite3.Cursor)
        self.connection.cursor.return_value = self.cursor
        self.db_handler = SQLiteDBHandler(self.connection)

    def test_get_table_sizes(self):
        self.cursor.fetchall.return_value = [("table1",), ("table2",)]
        self.cursor.fetchone.side_effect = [
            (4096,),  # page_size
            (10,),  # page_count for table1
            (15,),  # page_count for table2
        ]

        expected_result = {
            "table1": (10 * 4096) / (1024**2),  # Convert bytes to MB
            "table2": (15 * 4096) / (1024**2),  # Convert bytes to MB
        }

        result = self.db_handler.get_table_sizes()
        self.assertEqual(result, expected_result)

        self.cursor.execute.assert_any_call(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        self.cursor.execute.assert_any_call("PRAGMA page_size;")
        self.cursor.execute.assert_any_call("PRAGMA page_count('table1');")
        self.cursor.execute.assert_any_call("PRAGMA page_count('table2');")

    def test_get_row_counts(self):
        self.cursor.fetchall.return_value = [("table1",), ("table2",)]
        self.cursor.fetchone.side_effect = [
            (100,),  # row count for table1
            (200,),  # row count for table2
        ]

        expected_result = {
            "table1": 100,
            "table2": 200,
        }

        result = self.db_handler.get_row_counts()
        self.assertEqual(result, expected_result)

        self.cursor.execute.assert_any_call(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        self.cursor.execute.assert_any_call("SELECT COUNT(*) FROM table1")
        self.cursor.execute.assert_any_call("SELECT COUNT(*) FROM table2")


if __name__ == "__main__":
    unittest.main()
