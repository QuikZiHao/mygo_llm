import os
from langchain_openai import ChatOpenAI
from ..constants import LLM_CONFIG



def load_model() -> ChatOpenAI:
    os.environ["OPENAI_API_KEY"] = LLM_CONFIG.get("OPENAI_API_KEY","dummy-key")  # vLLM doesn't need a real API key
    os.environ["OPENAI_API_BASE"] = LLM_CONFIG.get("OPENAI_API_BASE","http://localhost:8000/v1")  # URL of your api
    model = LLM_CONFIG.get("model","gpt-4o-mini")

    # Initialize the LangChain OpenAI-compatible chat model
    llm = ChatOpenAI(
        temperature=0.7,
        model=model,  # Ensure this matches your vLLM-served model
        openai_api_key=LLM_CONFIG.get("OPENAI_API_KEY","dummy-key"),  # LangChain requires this even if it's a dummy value
    )
    return llm