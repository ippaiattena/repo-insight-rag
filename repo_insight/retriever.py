import shutil
import os
from langchain_chroma import Chroma
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.embeddings.base import Embeddings


def setup_retriever(persist_dir: str, embedder: Embeddings, reset: bool = False) -> VectorStoreRetriever:
    """ChromaのRetrieverを構築。必要に応じてDB削除"""
    if reset and os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedder)
    return vectordb.as_retriever()
