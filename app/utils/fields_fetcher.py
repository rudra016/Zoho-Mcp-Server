import requests
from typing import List
from .token_loader import load_token_from_client

def get_searchable_fields(module: str) -> List[str]:
    """
    Fetch field labels that are both searchable and visible from Zoho CRM for a given module.
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

    fields_data = response.json().get("fields", [])

    searchable_field_labels = [
        field["field_label"]
        for field in fields_data
        if field.get("searchable") and field.get("visible") and "field_label" in field
    ]

    return searchable_field_labels
