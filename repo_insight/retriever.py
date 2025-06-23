import glob
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.embeddings.base import Embeddings
import shutil
import os


def load_documents(local_path: str) -> list[Document]:
    """指定パス配下のファイルを読み込み、Documentリストに変換"""
    file_patterns = ["**/*.py", "**/*.md", "**/*.txt"]
    all_files = []
    for pattern in file_patterns:
        all_files.extend(glob.glob(os.path.join(local_path, pattern), recursive=True))
    docs = []
    for i, file in enumerate(all_files):
        print(f"[{i+1}/{len(all_files)}] 🔄 処理中: {file}")
        try:
            loader = TextLoader(file, encoding="utf-8")
            docs.extend(loader.load())
        except Exception as e:
            print(f"⚠️ 読み込み失敗: {file} ({e})")
    return docs


def setup_retriever(
    persist_dir: str,
    embedder: Embeddings,
    local_path: str = "./",
    reset: bool = False,
) -> VectorStoreRetriever:
    """ローカルファイルを走査してRetrieverを構築。必要に応じてDB削除"""
    if reset and os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    # ドキュメント読み込み & 分割
    raw_docs = load_documents(local_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(raw_docs)

    # ベクトルDB登録
    vectordb = Chroma.from_documents(split_docs, embedding=embedder, persist_directory=persist_dir)
    return vectordb.as_retriever()
