from pinecone import Pinecone, ServerlessSpec
from config.settings import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_REGION
import time

pc = Pinecone(api_key=PINECONE_API_KEY)

spec = ServerlessSpec(cloud="aws", region=PINECONE_REGION)
if PINECONE_INDEX_NAME not in [i.name for i in pc.list_indexes()]:
    pc.create_index(PINECONE_INDEX_NAME, dimension=768, metric="cosine", spec=spec)
    while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
        time.sleep(1)

pinecone_index = pc.Index(PINECONE_INDEX_NAME)
