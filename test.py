# import os
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts.chat import ChatPromptTemplate
# from langchain.schema import HumanMessage, SystemMessage
# from src.llm_process.constants import LLM_CONFIG_PATH
# from src.llm_process.utils.load_config import load_config
from src.llm_process.utils.rag_utils import get_embedded

# config = load_config(LLM_CONFIG_PATH)
# # Set environment variables for OpenAI-compatible API
# os.environ["OPENAI_API_KEY"] = config.get("OPENAI_API_KEY","dummy-key")  # vLLM doesn't need a real API key
# os.environ["OPENAI_API_BASE"] = config.get("OPENAI_API_BASE","http://localhost:8000/v1")  # URL of your api
# model = config.get("model","gpt-4o-mini")

# # Initialize the LangChain OpenAI-compatible chat model
# llm = ChatOpenAI(
#     temperature=0.7,
#     model=model,  # Ensure this matches your vLLM-served model
#     openai_api_key=config.get("OPENAI_API_KEY","dummy-key"),  # LangChain requires this even if it's a dummy value
# )

# # Create a chat prompt template
# prompt = ChatPromptTemplate.from_messages([SystemMessage(content="你是一個二次元角色助理"),HumanMessage(content="誰是御坂美琴")])

# # Generate a response
# response = llm.predict_messages(prompt.messages)
# print("Response:", response.content)
print(get_embedded("誰是御坂美琴"))