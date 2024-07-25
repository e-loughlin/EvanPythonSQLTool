import os
import unittest
from unittest.mock import MagicMock, patch

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

from binchicken.gpt import GPTQueryTool


class TestGPTQueryTool(unittest.TestCase):
    def setUp(self):
        # Set up test data
        self.api_key = "test_api_key"
        self.api_key = str(os.getenv("OPENAI_API_KEY"))
        self.gpt_tool = GPTQueryTool(openai_api_key=self.api_key, safe_mode=True)
        self.ibis_mock = MagicMock()
        self.ibis_mock.list_tables.return_value = ["table1", "table2"]

    @patch("openai.OpenAI")  # Mock OpenAI from the correct package
    def test_initialization(self, mock_openai):
        # Test if GPTQueryTool is initialized correctly
        tool = GPTQueryTool(self.api_key, safe_mode=False)
        self.assertEqual(tool.openai_api_key, self.api_key)
        self.assertFalse(tool.safe_mode)
        mock_openai.assert_called_once_with(api_key=self.api_key)

    def test_is_safe(self):
        # Test if _is_safe method correctly identifies safe and unsafe queries
        unsafe_queries = [
            "INSERT INTO table1 VALUES (1, 'test')",
            "UPDATE table1 SET column = 'value'",
            "DELETE FROM table1 WHERE column = 'value'",
            "DROP TABLE table1",
            "ALTER TABLE table1 ADD column new_column INT",
        ]
        safe_queries = [
            "SELECT * FROM table1",
            "SELECT column FROM table1 WHERE column = 'value'",
        ]
        for query in unsafe_queries:
            self.assertFalse(self.gpt_tool._is_safe(query))
        for query in safe_queries:
            self.assertTrue(self.gpt_tool._is_safe(query))

    def test_extract_sql_statement(self):
        # Test if _extract_sql_statement method correctly extracts SQL from markdown
        text = "```sql\nSELECT * FROM table1\n```"
        self.assertEqual(
            self.gpt_tool._extract_sql_statement(text), "SELECT * FROM table1"
        )
        text = "```sql\nSELECT column FROM table1 WHERE column = 'value'\n```"
        self.assertEqual(
            self.gpt_tool._extract_sql_statement(text),
            "SELECT column FROM table1 WHERE column = 'value'",
        )
        self.assertIsNone(self.gpt_tool._extract_sql_statement("No SQL block here"))

    @patch("openai.OpenAI")  # Mock OpenAI from the correct package
    def test_query(self, mock_openai):
        # Mock OpenAI API response
        mock_openai_instance = mock_openai.return_value
        mock_openai_instance.chat.completions.create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content="```sql\nSELECT * FROM table1\n```")
                )
            ]
        )

        # Test if the query method works as expected
        result = self.gpt_tool.query(
            self.ibis_mock, "Fetch all records from table1", execute=False
        )
        self.assertEqual(result, "SELECT * FROM table1")

        # Test if query is executed
        self.gpt_tool.query(
            self.ibis_mock, "Fetch all records from table1", execute=True
        )
        self.ibis_mock.sql.assert_called_once_with("SELECT * FROM table1")

        # Test if safe_mode prevents execution of unsafe queries
        self.gpt_tool.safe_mode = True
        unsafe_query = "INSERT INTO table1 VALUES (1, 'test')"
        with patch.object(
            self.gpt_tool, "_extract_sql_statement", return_value=unsafe_query
        ):
            with self.assertRaises(Exception) as context:
                self.gpt_tool.query(self.ibis_mock, "Unsafe query test", execute=True)
            self.assertIn("Unsafe SQL query detected", str(context.exception))

    @patch("openai.OpenAI")  # Mock OpenAI from the correct package
    def test_query_with_different_safe_mode(self, mock_openai):
        # Test if safe_mode disables execution of unsafe queries when set to False
        self.gpt_tool.safe_mode = False
        unsafe_query = "INSERT INTO table1 VALUES (1, 'test')"
        with patch.object(
            self.gpt_tool, "_extract_sql_statement", return_value=unsafe_query
        ):
            self.gpt_tool.query(self.ibis_mock, "Unsafe query test", execute=True)
            self.ibis_mock.sql.assert_called_once_with(unsafe_query)


if __name__ == "__main__":
    unittest.main()
