import numpy as np
from ..constants import LLM_CONFIG
from langchain_huggingface import HuggingFaceEmbeddings


def load_embedded_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=LLM_CONFIG.get("embedding_model"))
