from mcp.server.fastmcp import FastMCP
from prompts.descriptors import TOOL_DESCRIPTOR, FORMAT_INSTRUCTIONS
import requests
from typing import Dict
from utils.pinecone_client import pinecone_index
from utils.genai_client import embed_query

from utils.token_loader import load_token_from_client
import requests

mcp = FastMCP("zoho_crm")

   
@mcp.tool()
def get_filter_descriptors(question: str, module: str = "Deals", complexity: str = "simple") -> Dict:
    """
    This tool performs a Pinecone vector search based on the question and module,
    and returns matching content, tool descriptors, and formatting instructions.
    """
    try:
        print(f"Tool received question: {question}")

        vector = embed_query(question)
        top_k = 8 if complexity == "simple" else 10
        pinecone_results = pinecone_index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            filter={"module": module}
        )

        field_hints = [
            f"{m['metadata']['content']}\n\nSimilarity Score: {m.get('score', 0):.4f}"
            for m in pinecone_results['matches']
            if 'content' in m['metadata']
        ]

        return {
            "pinecone_results": field_hints,
            "descriptors": TOOL_DESCRIPTOR,
            "format_instructions": FORMAT_INSTRUCTIONS
        }

    except Exception as e:
        import traceback
        print("Tool crashed:", traceback.format_exc())
        return {
            "error": "Tool failed internally",
            "details": str(e)
        }


@mcp.tool()
def fetch_zoho_results(url: str) -> dict:
    """
    This tool makes a request to Zoho CRM using the provided URL.
    The URL should be constructed by the LLM using the descriptors and format instructions from the get_filter_descriptors tool.
    """
    try:
        print(f"Tool received URL: {url}")
        
        # Load token data
        token_data = load_token_from_client()
        access_token = token_data["access_token"]
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return {
            "results": response.json()
        }
    except Exception as e:
        import traceback
        print("Tool crashed:", traceback.format_exc())
        return {"error": "Tool failed internally", "details": str(e)}

if __name__ == "__main__":
    mcp.run(transport="sse")