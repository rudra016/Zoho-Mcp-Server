import requests
from typing import List, Dict
from .token_loader import load_token_from_client


def get_field_metadata(module: str) -> List[Dict]:
    """
    Fetch all fields (not just searchable) for the specified module.
    """
    token_data = load_token_from_client()
    access_token = token_data["access_token"]
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    url = f"https://www.zohoapis.com/crm/v7/settings/fields?module={module}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Zoho field API failed with status {response.status_code}: {response.text}")

    return response.json().get("fields", [])


def get_searchable_fields(module: str) -> List[str]:
    """
    Returns the list of searchable & visible field labels for a module.
    """
    all_fields = get_field_metadata(module)
    return [
        field["field_label"]
        for field in all_fields
        if field.get("searchable") and field.get("visible") and "field_label" in field
    ]

