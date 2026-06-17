from langchain_openai import OpenAIEmbeddings
from config.settings import settings

def get_embeddings():
    embeddings = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        openai_api_key=settings.OPENAI_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    return embeddings