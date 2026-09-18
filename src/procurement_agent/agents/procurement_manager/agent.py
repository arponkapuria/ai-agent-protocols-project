from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
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

pricing_agent = RemoteA2aAgent(
    name="vendor_pricing_agent",
    description="Gets price quotes for components across vendors.",
    agent_card="http://localhost:8001/.well-known/agent-card.json",
)

quality_agent = RemoteA2aAgent(
    name="vendor_quality_agent",
    description="Gets vendor quality/reliability ratings.",
    agent_card="http://localhost:8002/.well-known/agent-card.json",
)

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="procurement_manager",
    instruction=(
        "You manage procurement for JAMC Manufacturing. "
        "Use check_inventory/list_low_stock for stock. "
        "When asked to compare vendors, you MUST query BOTH vendor_pricing_agent AND vendor_quality_agent before giving a recommendation — price alone is not sufficient. "
        "When querying vendor_quality_agent, use canonical vendor IDs like 'vendor_a' and 'vendor_b', not display names."
    ),
    tools=[inventory_tools],
    sub_agents=[pricing_agent, quality_agent],
)