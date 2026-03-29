
import os
from dotenv import load_dotenv
from nemoguardrails import RailsConfig, LLMRails
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Create MCP server
mcp = FastMCP("guardrail-server")

# Load NeMo Guardrails config
config = RailsConfig.from_path("./mcp_server/guardrails")

# Initialize guardrails engine
rails = LLMRails(config,verbose=True)
# rails.llm.completion_kwargs = {}




# MCP TOOL
@mcp.tool(
    name="guarded_chat",
    description="Use this tool for ALL user prompts. Applies safety guardrails before answering."
)
async def guarded_chat(prompt: str) -> str:

    print("Tool invoked")
 
    try:

        # Run through NeMo Guardrails
        response = await rails.generate_async(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        explain = rails.explain()
        explain.print_llm_calls_summary()


        # Handle response format
        if isinstance(response, dict):
            return response.get("content", str(response))

        return str(response)

    except Exception as e:

        return f"Guardrail processing error: {str(e)}"


# Start MCP server
if __name__ == "__main__":

    print("API BASE:", os.getenv("OPENAI_API_BASE"))
    print("API KEY:", os.getenv("OPENAI_API_KEY")[:10])

    print("#############################")
    print("GUARDRAIL MCP Server started")
    print("#############################")

    mcp.run()

