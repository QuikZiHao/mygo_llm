from typing import List
from ..utils.solve_data import solve_data
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from langchain_community.document_loaders import PebbloTextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def bind_embedding(db: PGVector) -> List:
    result = solve_data()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
    loader = PebbloTextLoader(texts=result["texts"],
                            metadatas=result["episodes"],)
    docs = loader.load()
    splits = text_splitter.split_documents(docs)
    return db.add_documents(splits,ids=[str(idx+1) for idx in range(len(splits))])
