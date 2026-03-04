from mcp.server.fastmcp import FastMCP

#Initialize the MCP Server
mcp = FastMCP("SalesIntelligence")

@mcp.tool()
def get_revenue_by_region(region: str) -> str:
    """Returns the total revenue for a specific region (North, South, East, West)."""
    # Placeholder implementation
    revenue_data = {
        "North": "$450k",
        "South": "$320k",
        "East": "$510k",
        "West": "$290k"
    }
    return f"Revenue for the {region} region is ${revenue_data.get(region, 'unknown')}."

if __name__ == "__main__":
    mcp.run(transport="stdio")