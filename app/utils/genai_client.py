import google.generativeai as genai
from config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def embed_query(text: str) -> list:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query",
    )
    return result['embedding']

def start_chat(model_name="gemini-1.5-pro"):
    return genai.GenerativeModel(model_name).start_chat()
