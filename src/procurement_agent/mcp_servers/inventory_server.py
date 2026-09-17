# Turns a SQLite inventory database into an MCP server with two AI-callable tools.

import sqlite3
from mcp.server.mcpserver import MCPServer
from db import DB_PATH, init_db


init_db()
mcp = MCPServer("jamc-inventory")

def _query(sql: str, params: tuple = ()):
    """Opens the database and executes a sql query"""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    return [dict(r) for r in rows]

@mcp.tool()
def check_inventory(component: str) -> dict:
    """Check current stock level and reorder threshold for a component."""

    rows = _query("SELECT * FROM inventory WHERE component = ?", (component,))
    if not rows:
        return {"error": f"Unknown component: {component}"}

    row = rows[0]
    row["needs_reorder"] = row["quantity"] < row["reorder_threshold"]
    return row

@mcp.tool()
def list_low_stock() -> list[dict]:
    """List all components currently below their reorder threshold."""
    return _query("SELECT * FROM inventory WHERE quantity < reorder_threshold")


if __name__ == "__main__":
    mcp.run(transport="stdio")