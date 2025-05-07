from mcp.server.fastmcp import FastMCP
from prompts.descriptors import TOOL_DESCRIPTOR, FORMAT_INSTRUCTIONS
import requests
from typing import Dict
from utils.pinecone_client import pinecone_index
from utils.genai_client import embed_query
from utils.fields_fetcher import get_searchable_fields, get_field_metadata
from utils.token_loader import load_token_from_client
import requests

mcp = FastMCP("zoho_crm")

@mcp.tool()
def get_filter_descriptors(question: str, module: str = "Deals", complexity: str = "simple") -> Dict:
    """
    Performs a Pinecone vector search on the given question using searchable fields,
    and returns matched field hints. If a field is a picklist, includes its values.
    """
    try:
        print(f"Tool received question: {question}")
        searchable_fields = get_searchable_fields(module)
        print(f"Searchable fields for {module}: {searchable_fields}")

        if not searchable_fields:
            return {
                "pinecone_results": [],
                "descriptors": TOOL_DESCRIPTOR,
                "format_instructions": FORMAT_INSTRUCTIONS,
                "warning": f"No searchable fields found for module '{module}'"
            }

        vector = embed_query(question)
        top_k = 8 if complexity == "simple" else 10

        pinecone_results = pinecone_index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            filter={
                "module": module,
                "field_name": {"$in": searchable_fields}
            }
        )

        # Fetch full metadata to match picklists
        field_metadata = get_field_metadata(module)
        metadata_lookup = {field["field_label"]: field for field in field_metadata}

        field_hints = []
        for match in pinecone_results['matches']:
            metadata = match.get("metadata", {})
            field_label = metadata.get("field_name", "")
            content = metadata.get("content", "")
            score = match.get("score", 0.0)

            picklist_values = []
            if field_label in metadata_lookup:
                field_info = metadata_lookup[field_label]
                if field_info.get("data_type") == "picklist":
                    picklist_values = [
                        item.get("actual_value")
                        for item in field_info.get("pick_list_values", [])
                        if item.get("actual_value") is not None
                    ]

            result_text = f"{content}\n\nSimilarity Score: {score:.4f}"
            if picklist_values:
                result_text += f"\nPicklist Values: {picklist_values}"

            field_hints.append(result_text)

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
        return {
        "results": {
            "error": "Tool failed internally",
            "details": str(e),
            "trace": traceback.format_exc()
        }
    }

if __name__ == "__main__":
    mcp.run(transport="sse")