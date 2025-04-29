from pydantic import BaseModel

class ZohoToken(BaseModel):
    access_token: str
    refresh_token: str
    api_domain: str
    token_type: str
    expires_in: int
