import requests

def load_token_from_client() -> dict:
    FASTAPI_TOKEN_URL = "https://zoho-mcp-fastapi.onrender.com/token"

    try:
        res = requests.get(FASTAPI_TOKEN_URL)
        res.raise_for_status()
        token_data = res.json()

        if "error" in token_data:
            raise Exception("Token fetch error: No valid token found.")

        return token_data

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching token from FastAPI server: {str(e)}")
