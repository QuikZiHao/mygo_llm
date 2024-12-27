from ..utils.rag_utils import load_embedded_model
from langchain_postgres import PGVector
from ..constants import LLM_CONFIG

def load_vectordb() -> PGVector:
    return  PGVector(
    embeddings=load_embedded_model(),
    collection_name=LLM_CONFIG.get("collection_name"),
    connection=LLM_CONFIG.get("db_connection"),
    use_jsonb=True,
    )   