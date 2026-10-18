from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Notes Assistant")


# Import tools so they get registered
from app.mcp import tools

if __name__ == "__main__":
    mcp.run()