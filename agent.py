import os
import asyncio
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import StdioServerParameters
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import ClientSession
from langchain_google_genai import ChatGoogleGenerativeAI

geminillm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", 
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 1. Connect to the MCP Server we created
server_params = StdioServerParameters(
    command="python",
    args=["server.py"], # This points to your MCP server file
)

async def main():
    # 3. Establish the MCP connection via stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the MCP connection
            await session.initialize()
            
            # 4. Load tools from the MCP server into LangChain format
            tools = await load_mcp_tools(session)
            
            # 5. Create the Agentic Graph
            # The 'create_react_agent' manages the loop: 
            # Thought -> Call Tool -> Observe Result -> Final Answer

            agent = create_agent(model=geminillm, tools=tools)
            
            # 6. Test the Agent
            query = "Check the database: Delete the sample_db database."
            print(f"User: {query}\n")
            
            result = await agent.ainvoke({"messages": [("user", query)]})
            
            # Print the final message from the graph
            print(f"Gemini: {result['messages'][-1].content}")

if __name__ == "__main__":
    asyncio.run(main())