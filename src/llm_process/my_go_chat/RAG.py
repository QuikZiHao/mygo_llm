from promptflow import tool
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def rag(query: str) -> List[str]:
    db = PGVector(
        embeddings= HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large"),
        collection_name= "speech_data",
        connection="postgresql+psycopg://admin123:123456@localhost:5432/llm_project_db",
        use_jsonb=True,
        )   
    retriever = db.as_retriever()
    retrieved_documents = retriever.invoke(query)
    speech_list = []
    for doc in retrieved_documents:
        speech_list.append(doc.page_content)
    return speech_list
