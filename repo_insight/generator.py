from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.vectorstores.base import VectorStoreRetriever

def build_qa_chain(retriever: VectorStoreRetriever) -> RetrievalQA:
    """
    LLM（ChatGPT）とRetrieverを使って質問応答チェーンを構築する。

    Parameters:
    - retriever: ベクトル検索用のRetriever

    Returns:
    - RetrievalQA: 質問に対して回答を返すチェーン
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
