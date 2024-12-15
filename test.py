import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import HumanMessage

# Set environment variables for OpenAI-compatible API
os.environ["OPENAI_API_KEY"] = "dummy_api_key"  # vLLM doesn't need a real API key
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"  # URL of your vLLM server

# Initialize the LangChain OpenAI-compatible chat model
llm = ChatOpenAI(
    temperature=0.7,
    model="Llama-3.2-1B",  # Ensure this matches your vLLM-served model
    openai_api_key="dummy_api_key",  # LangChain requires this even if it's a dummy value
)

# Create a chat prompt template
prompt = ChatPromptTemplate.from_messages([HumanMessage(content="Hello, who are you?")])

# Generate a response
response = llm.predict_messages(prompt.messages)
print("Response:", response.content)
