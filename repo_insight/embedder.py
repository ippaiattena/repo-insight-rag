import os
import shutil
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from repo_insight.utils.env import load_api_key

def load_embedder() -> OpenAIEmbeddings:
    """
    OpenAI APIキーを読み込んで Embeddings オブジェクトを返す。
    """
    api_key = load_api_key()
    os.environ["OPENAI_API_KEY"] = api_key
    return OpenAIEmbeddings()

def create_vector_store(persist_dir: str, embedder: OpenAIEmbeddings) -> None:
    """
    指定ディレクトリにベクトルストアを作成・保存する。

    Parameters:
    - persist_dir: ベクトルストアの保存先ディレクトリ
    - embedder: OpenAIEmbeddings インスタンス
    """

    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    vectordb = Chroma(embedding_function=embedder, persist_directory=persist_dir)
    vectordb.add_texts(["これはサンプル文書です。埋め込みのテストです。"])
    print(f"✅ ベクトルストアを保存しました → {persist_dir}")
