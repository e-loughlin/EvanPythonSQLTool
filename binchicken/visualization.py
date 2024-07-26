from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
from db_handler import DBHandler


class DatabaseVisualizer(ABC):
    @abstractmethod
    def visualize_table_sizes(self):
        pass

    @abstractmethod
    def visualize_row_counts(self):
        pass

    @abstractmethod
    def visualize_index_usage(self):
        pass

    @abstractmethod
    def visualize_query_performance(self):
        pass


class DatabaseVisualizer(DatabaseVisualizer):
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

    def visualize_index_usage(self):
        index_usage = self.db_handler.get_index_usage()
        indexes = list(index_usage.keys())
        usage_counts = list(index_usage.values())

        plt.figure(figsize=(10, 5))
        plt.bar(indexes, usage_counts, color="salmon")
        plt.xlabel("Indexes")
        plt.ylabel("Usage Count")
        plt.title("Index Usage")
        plt.xticks(rotation=45)
        plt.show()

    def visualize_query_performance(self):
        query_performance = self.db_handler.get_query_performance()
        queries = list(query_performance.keys())
        times = list(query_performance.values())

        plt.figure(figsize=(10, 5))
        plt.bar(queries, times, color="lightblue")
        plt.xlabel("Queries")
        plt.ylabel("Execution Time (ms)")
        plt.title("Query Performance")
        plt.xticks(rotation=45)
        plt.show()
