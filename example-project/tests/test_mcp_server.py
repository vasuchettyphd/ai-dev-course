"""Tests for the MCP server (week 11). They start the real server as a separate program and
talk to it over stdio with the MCP package's own client, the way Claude Code would. No key
and no network. Skipped if the MCP package isn't installed (it needs Python 3.11 or newer).
"""
import asyncio
import json
import pathlib
import sys
import tempfile
import unittest

try:
    from mcp import Client, StdioServerParameters
except ImportError:
    Client = None

PROJECT = pathlib.Path(__file__).parent.parent
LISTING_B = {"purchase_price": 150000, "monthly_rent": 1700, "yearly_property_tax": 2400,
             "yearly_insurance": 1200, "monthly_hoa": 0, "down_payment_pct": 25,
             "interest_rate_pct": 7, "loan_term_years": 30, "closing_costs": 6000}


def talk_to_server(action, cwd=PROJECT, env=None):
    """Start the server, run action(client) and return what it returns."""
    async def session():
        server = StdioServerParameters(command=sys.executable, args=["-m", "dealscreener.mcp_server"],
                                       cwd=str(cwd), env=env)
        async with Client(server) as client:
            return await action(client)
    return asyncio.run(session())


def text_of(result):
    return "\n".join(item.text for item in result.content if getattr(item, "type", None) == "text")


@unittest.skipIf(Client is None, "the MCP package isn't installed (pip install -r requirements.txt)")
class McpServerTest(unittest.TestCase):
    def test_lists_one_tool_with_the_nine_numbers(self):
        listed = talk_to_server(lambda client: client.list_tools())
        self.assertEqual([tool.name for tool in listed.tools], ["screen_listing"])
        tool = listed.tools[0]
        self.assertIn("percentages are written as 25 for 25%", tool.description)
        schema = tool.input_schema if hasattr(tool, "input_schema") else tool.inputSchema
        self.assertEqual(sorted(schema["required"]), sorted(LISTING_B))
        self.assertIn("description", schema["properties"]["interest_rate_pct"])

    def test_starts_from_another_folder_with_pythonpath(self):
        # Claude Code may start the server in a different folder: the README's command sets
        # PYTHONPATH to the project folder so Python still finds the dealscreener package.
        with tempfile.TemporaryDirectory() as elsewhere:
            listed = talk_to_server(lambda client: client.list_tools(), cwd=elsewhere,
                                    env={"PYTHONPATH": str(PROJECT)})
        self.assertEqual([tool.name for tool in listed.tools], ["screen_listing"])

    def test_listing_b_gives_its_cash_flow(self):
        result = talk_to_server(lambda client: client.call_tool("screen_listing", LISTING_B))
        self.assertFalse(result.is_error if hasattr(result, "is_error") else result.isError)
        self.assertIn("430.53", text_of(result))
        self.assertEqual(json.loads(text_of(result))["overall"], "PASS")

    def test_a_percentage_written_as_a_fraction_comes_back_as_an_error(self):
        bad = dict(LISTING_B, interest_rate_pct=0.07)
        result = talk_to_server(lambda client: client.call_tool("screen_listing", bad))
        self.assertTrue(result.is_error if hasattr(result, "is_error") else result.isError)
        self.assertIn("percentages are written as 7 for 7%", text_of(result))

    def test_text_instead_of_a_number_comes_back_as_an_error(self):
        bad = dict(LISTING_B, monthly_rent="1700")
        result = talk_to_server(lambda client: client.call_tool("screen_listing", bad))
        self.assertTrue(result.is_error if hasattr(result, "is_error") else result.isError)
        self.assertIn("monthly_rent", text_of(result))


if __name__ == "__main__":
    unittest.main()
