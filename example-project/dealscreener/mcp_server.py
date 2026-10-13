"""The deal screener as an MCP server (week 11): Claude Code, or any MCP app, can call the
screen_listing tool.

  python -m dealscreener.mcp_server

It talks over stdio (standard input and output), so running it by hand just waits silently
for an app to connect: press Ctrl+C to stop it. Usually Claude Code starts it for you (see
the README). It needs no API key and reads no .env file: the tool only calculates.

It needs the MCP package (pip install -r requirements.txt) and Python 3.11 or newer.
Version 2 of the package calls the server class MCPServer (older tutorials say FastMCP).
"""
from typing import Annotated

from pydantic import Field

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from dealscreener import tools

DESCRIPTIONS = {field: spec["description"]
                for field, spec in tools.TOOL_SCHEMA["input_schema"]["properties"].items()}

mcp = MCPServer("dealscreener")


def number(field):
    """A number parameter with the tool's own description. strict=True stops the package
    turning text like "1700" into a number before our own check sees it."""
    return Annotated[float, Field(strict=True, description=DESCRIPTIONS[field])]


@mcp.tool(name=tools.TOOL_NAME, description=tools.TOOL_SCHEMA["description"])
def screen_listing(
    purchase_price: number("purchase_price"),
    monthly_rent: number("monthly_rent"),
    yearly_property_tax: number("yearly_property_tax"),
    yearly_insurance: number("yearly_insurance"),
    monthly_hoa: number("monthly_hoa"),
    down_payment_pct: number("down_payment_pct"),
    interest_rate_pct: number("interest_rate_pct"),
    loan_term_years: Annotated[int, Field(strict=True, description=DESCRIPTIONS["loan_term_years"])],
    closing_costs: number("closing_costs"),
) -> dict:
    # The same checks and numbers as the agent's tool. A problem is raised as the package's
    # ToolError, so it comes back to the app as an error result holding our sentence (any
    # other error would come back as just "Error executing tool screen_listing").
    try:
        return tools.screen_listing(dict(
            purchase_price=purchase_price, monthly_rent=monthly_rent,
            yearly_property_tax=yearly_property_tax, yearly_insurance=yearly_insurance,
            monthly_hoa=monthly_hoa, down_payment_pct=down_payment_pct,
            interest_rate_pct=interest_rate_pct, loan_term_years=loan_term_years,
            closing_costs=closing_costs,
        ))
    except tools.ToolInputError as problem:
        raise ToolError(str(problem)) from None


if __name__ == "__main__":
    mcp.run()  # stdio is the default transport
