import re

from openai import OpenAI


class GPTQueryTool:
    def __init__(self, openai_api_key: str, safe_mode: bool = True):
        self.openai_api_key = openai_api_key
        self.safe_mode = safe_mode  # Prevents mutations to DB if safe_mode is True

        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=openai_api_key)

    def _is_safe(self, query):
        """
        Returns whether a SQL query is safe to execute, i.e. whether it has mutable effects on the DB.
        """
        query = query.lower()
        if (
            "insert" in query
            or "update" in query
            or "delete" in query
            or "drop" in query
            or "alter" in query
        ):
            return False
        return True

    def _extract_sql_statement(self, text):
        pattern = r"```sql\s+([^`]+)\s+```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def query(self, ibisDB, user_prompt: str, execute: bool = False):
        """
        Generate and optionally execute a SQL query using OpenAI GPT.

        This method accepts an Ibis database connection and a user prompt, then queries
        OpenAI GPT to build a SQL query based on the provided schema. If `execute` is True,
        it will run the generated SQL query. Otherwise, it will prompt the user to confirm.

        Parameters:
        ibisDB (ibis.client.Client): The Ibis database connection.
        user_prompt (str): The user's query prompt for generating the SQL query.
        execute (bool): If True, execute the generated SQL query. Defaults to False.

        Returns:
        pd.DataFrame: The result of the executed SQL query as a pandas DataFrame.

        Raises:
        Exception: If the generated SQL query is deemed unsafe and `safe_mode` is enabled.
        """
        # Construct the database schema string
        schema_string = "The DB Schema is as follows:\n"
        for table in ibisDB.list_tables():
            schema_string += f"{table}\n\n"

        # Prepare the messages for the OpenAI chat API
        messages = [
            {
                "role": "system",
                "content": f"Here is the DB structure:\n\n{schema_string}\n\nThe query is specified below. Respond with the query in SQL format.",
            },
            {
                "role": "user",
                "content": f"Generate the following SQL query: {user_prompt}.\n\nFormat the response as SQL and say NOTHING else.",
            },
        ]

        # Query the OpenAI API
        completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages, max_tokens=4096
        )

        # Extract the response text
        response_text = completion.choices[0].message.content

        print(f"Raw response from ChatGPT: {response_text}")
        sql_query = self._extract_sql_statement(response_text)

        print(f"Generated SQL:\n\n{sql_query}\n")

        # Check for safe mode
        if self.safe_mode and not self._is_safe(sql_query):
            raise Exception(
                f"Unsafe SQL query detected: {sql_query}\n"
                "Will not execute as long as safe_mode = True"
            )

        # Optionally execute the SQL query
        if execute:
            return ibisDB.sql(sql_query).to_pandas()
        else:
            return sql_query
