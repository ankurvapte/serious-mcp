import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

server_params = StdioServerParameters(
                                        command="python",
                                        args=["sales_server.py"]
                                    )

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 3. Automatically discover and load tools from the MCP server
            mcp_tools = await load_mcp_tools(session)

            # 4. Create LangGraph Agent
            model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key="AIzaSyDSXec1qp7h2BcYDWlwdtvGW958fx_o9NQ")
            agent = create_agent(model=model, tools=mcp_tools)

            # 5. Execute a task
            query = "Compare the revenue of the North and West regions."
            print(f" --- Calling Gemini Agent : '{query}' --- ")
            result = await agent.ainvoke({
                "messages": [("user", query)]
            })

            print("\nFinal Answer:")
            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(run_agent())
