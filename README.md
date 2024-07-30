# Bin Chicken DB Library

<p align="center">
<img src="bin_chicken_logo.png" style="display: block; margin: 0 auto; width: 200px; height: 200px;">
</p>

## Overview
Bin Chicken is a simple Python library wrapping the [Ibis Library](https://ibis-project.org/) designed to help data scientists and engineers streamline their SQL-related tasks and enhance their workflow efficiency. This library aims to provide a foundational toolset for analyzing experiments, fetching data, building insights, and standardizing repeatable data science tasks.

### Naming

"Bin Chicken" is an Australian colloquial term to refer to the Australian White Ibis, due to its habit of eating from rubbish bins.

### Features

[- GPT Query Tool](#gpt-query-tool)
  - Run SQL commands on your Ibis Database Connection with a user prompt query.
[- Visualization](#visualization)
  - Basic visualization library outputting simple graphs for SQLite Databases.


## Getting Started

### Create a Virtual Environment

```bash
python -m venv venv
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## GPT Query Tool

GPTQueryTool allows you to execute SQL queries from a text prompt. It returns resulting Pandas Dataframes, if they exist.
By default, `safe_mode` is on and prevents SQL queries that contain any mutations or alterations. 

⚠️  **Use at your own risk!** ⚠️ 

```python
import sys
import os
import ibis
from IPython.display import display, Markdown

# Add the library path
sys.path.append(os.path.abspath('../binchicken'))

# Import the GPT query tool
from gpt import GPTQueryTool

# Load the .env file
from dotenv import load_dotenv
load_dotenv()

# Get the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

# Connect to a SQLite database
conn = ibis.connect("sqlite://sakila.db")

# Initialize the GPT query tool
gpt_tool = GPTQueryTool(
    openai_api_key,
    safe_mode=True
)

# Run a query
result = gpt_tool.query(
    conn, 
    "Find all actors whose last names contain the letters LI. Order the rows by last name and first name, in that order",
    execute=True
)

# Display the results
display(result)

```

Generated SQL: 

```sql

SELECT * FROM actor
WHERE last_name LIKE '%LI%'
ORDER BY last_name, first_name;
```

Resulting in the following Pandas Dataframe:

actor_id | first_name | last_name | last_update
--- | --- | --- | ---
86 | GREG | CHAPLIN | 2020-12-23 07:12:30
82 | WOODY | JOLIE | 2020-12-23 07:12:30
34 | AUDREY | OLIVIER | 2020-12-23 07:12:29
15 | CUBA | OLIVIER | 2020-12-23 07:12:29
172 | GROUCHO | WILLIAMS | 2020-12-23 07:12:31
137 | MORGAN | WILLIAMS | 2020-12-23 07:12:30
72 | SEAN | WILLIAMS | 2020-12-23 07:12:29
83 | BEN | WILLIS | 2020-12-23 07:12:30
96 | GENE | WILLIS | 2020-12-23 07:12:30
164 | HUMPHREY | WILLIS | 2020-12-23 07:12:31


### Additional Parameters

`safe_mode`:
The safe_mode parameter in the GPTQueryTool initialization is used to ensure that the queries executed are safe and secure. When safe_mode=True, the tool performs additional checks to avoid potentially harmful operations and to ensure the queries do not cause unintended changes or access restricted data. This is particularly useful in environments where query safety is a concern.

`execute`:
The execute parameter in the query method determines whether the generated SQL query should be executed immediately. When execute=True, the query is sent to the database and the results are returned. If execute=False, the query is only generated and returned as a string, allowing you to review or modify it before running it manually.

### GPTQueryTool Examples

Refer to the [Jupyter Notebook 03_GPTQueryTool Examples](https://github.com/e-loughlin/bin-chicken/blob/main/playground/03_GPTQueryTool.ipynb) for more examples of how to use this feature.

## Visualization

This is a simple visualization library, primarily developed to demonstrate OOP in Python, with associated unit tests. 
It utilizes abstract classes for DB_Handler (which can be extended easily to other DB types) which then is used by the Visualization tool to produce simple graphs.

```python
import pandas as pd
import ibis
import sqlite3
import sys, os 

# Bin Chicken Imports
sys.path.append(os.path.abspath('../binchicken'))
from visualization import DatabaseVisualizer
from db_handler import SQLiteDBHandler


# Connect to the SQLite database
connection = sqlite3.connect('sakila.db')

# Initialize the SQLiteDBHandler with the connection
sqlite_db_handler = SQLiteDBHandler(connection)

# Initialize the DatabaseVisualizer with the DBHandler
db_visualizer = DatabaseVisualizer(sqlite_db_handler)

# Visualize table sizes
db_visualizer.visualize_table_sizes()

# Visualize row counts
db_visualizer.visualize_row_counts()

```

![./playground/row_counts.png]

An example can be found here: [Jupyter - Visualization and OOP Demo](https://github.com/e-loughlin/bin-chicken/blob/main/playground/04_Python_Inheritance_Practice.ipynb).
