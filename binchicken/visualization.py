from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
from db_handler import DBHandler


class IDatabaseVisualizer(ABC):
    @abstractmethod
    def visualize_table_sizes(self):
        pass

    @abstractmethod
    def visualize_row_counts(self):
        pass


class DatabaseVisualizer(IDatabaseVisualizer):
    def __init__(self, db_handler: DBHandler):
        self.db_handler = db_handler

    def visualize_table_sizes(self):
        sizes = self.db_handler.get_table_sizes()
        tables = list(sizes.keys())
        size_values = list(sizes.values())

        plt.figure(figsize=(10, 5))
        plt.bar(tables, size_values, color="skyblue")
        plt.xlabel("Tables")
        plt.ylabel("Size (MB)")
        plt.title("Table Sizes")
        plt.xticks(rotation=45)
        plt.show()

    def visualize_row_counts(self):
        row_counts = self.db_handler.get_row_counts()
        tables = list(row_counts.keys())
        counts = list(row_counts.values())

        plt.figure(figsize=(10, 5))
        plt.bar(tables, counts, color="lightgreen")
        plt.xlabel("Tables")
        plt.ylabel("Row Count")
        plt.title("Row Counts per Table")
        plt.xticks(rotation=45)
        plt.show()
