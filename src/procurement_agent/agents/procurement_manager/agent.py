from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from dotenv import load_dotenv
import sys, pathlib

load_dotenv()

# absolute path to our server script
SERVER_PATH = str(
    pathlib.Path(__file__).resolve().parents[2] / "mcp_servers" / "inventory_server.py"
)

inventory_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,   # run with the same venv's python
            args=[SERVER_PATH],
        ),
        timeout=30,
    )
)

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="procurement_manager",
    instruction=(
        "You manage procurement for JAMC (Just Another Manufacturing Company)."
        "Use check_inventory or list_low_stock to answer stock questions truthfully — "
        "never guess numbers."
    ),
    tools=[inventory_tools],
)