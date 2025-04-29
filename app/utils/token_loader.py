import json
import os

def load_token_from_client() -> dict:
    token_path = os.path.join("..", "client", "token_store.json")
    if not os.path.exists(token_path):
        raise FileNotFoundError("token_store.json not found.")
    
    with open(token_path, "r") as f:
        return json.load(f)
