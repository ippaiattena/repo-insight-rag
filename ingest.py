import os
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.embeddings.base import Embeddings
from repo_insight.embedder import load_embedder
from repo_insight.utils.project_structure import get_project_structure
from repo_insight.retriever import load_documents

def ingest_repo_structure(repo_name: str, local_path: str, persist_dir: str):
    # 1. 構造情報の取得
    structure_text = get_project_structure(local_path)
    if not structure_text.strip():
        print("⚠️ 構造情報が空です。スキップします。")
        return

    # 2. 仮想ドキュメント化
    doc = Document(
        page_content=structure_text,
        metadata={"source": "project_structure.txt", "type": "structure"}
    )

    # 3. 分割（通常のコードファイルと同様）
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents([doc])

    # 4. 埋め込み & 保存
    embedder = load_embedder()
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedder
    )
    vectordb.add_documents(splits)

    print(f"✅ 構成情報を埋め込みました → {persist_dir}/project_structure.txt")


def ingest_all(local_path: str, persist_dir: str, embedder: Embeddings):
    # コードファイル埋め込み
    raw_docs = load_documents(local_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(raw_docs)

    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedder)
    vectordb.add_documents(split_docs)

    # プロジェクト構造も埋め込み
    ingest_repo_structure(repo_name=os.path.basename(local_path), local_path=local_path, persist_dir=persist_dir)
