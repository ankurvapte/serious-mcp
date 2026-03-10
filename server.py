import sqlite3
from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("SQLite Explorer")

DB_PATH = "sample_data.db"

def init_db():
    """Initialize a dummy database for the POC."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
        conn.execute("INSERT OR IGNORE INTO users (id, name, role) VALUES (1, 'Alice', 'Admin'), (2, 'Bob', 'Dev')")
        conn.commit()

@mcp.tool()
def list_tables() -> str:
    """List all tables in the database to understand the schema."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        return f"Tables: {', '.join(tables)}"

@mcp.tool()
def run_query(query: str) -> str:
    """
    Execute a read-only SQL query and return results.
    Args:
        query: A valid SELECT SQL statement.
    """
    if not query.lower().strip().startswith("select"):
        return "Error: Only SELECT queries are allowed for safety."
        
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            return str(rows)
    except Exception as e:
        return f"Database Error: {str(e)}"

if __name__ == "__main__":
    init_db()
    # MCP uses stdio by default for communication
    mcp.run()