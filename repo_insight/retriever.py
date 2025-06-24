import glob
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_chroma import Chroma
from langchain.vectorstores import Chroma
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.embeddings.base import Embeddings
import shutil
import os
from langchain.schema import Document
from repo_insight.utils.project_structure import get_project_structure
import gc
import time
from repo_insight.settings import get_shared_settings

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

def safe_remove_dir(path: str):
    try:
        shutil.rmtree(path)
        print(f"✅ ディレクトリ削除成功: {path}")
    except Exception as e:
        print(f"⚠️ ディレクトリ削除失敗: {e}")

def setup_retriever(
    persist_dir: str,
    embedder: Embeddings,
    local_path: str = "./",
    reset: bool = False,
) -> VectorStoreRetriever:
    """ローカルファイルを走査してRetrieverを構築。必要に応じてDB削除"""
    if reset and os.path.exists(persist_dir):
        # Chroma DB を使っているプロセスがあると削除できないため、先に開いて閉じる
        try:
            # 一度ロードして開放
            tmp_db = Chroma(
                persist_directory=persist_dir,
                embedding_function=embedder,
                client_settings=get_shared_settings(persist_dir)
            )
            # 明示的にクライアントを閉じる
            if hasattr(tmp_db, "_client") and hasattr(tmp_db._client, "reset"):
                tmp_db._client.reset()  # Chromaのclientの接続をリセット
                print("🔄 DB接続をリセットしました。")

            del tmp_db
            tmp_db = None
            gc.collect()
            time.sleep(5)  # Windows用ファイル解放待機
        except Exception as e:
            print(f"⚠️ DB初期化前の開放に失敗: {e}")
        
        safe_remove_dir(persist_dir)

    # ドキュメント読み込み & 分割
    raw_docs = load_documents(local_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(raw_docs)

    # プロジェクト構成情報もドキュメントとして追加
    structure_text = "[PROJECT_STRUCTURE]\nこれはプロジェクト構成情報です。\n" + get_project_structure(local_path)
    if structure_text.strip():
        structure_doc = Document(
            page_content=structure_text,
            metadata={"source": "project_structure.txt", "type": "structure"}
        )
        structure_splits = splitter.split_documents([structure_doc])
        split_docs.extend(structure_splits)
        print(f"✅ 構成情報も retriever に含めました。")

    # ベクトルDB登録
    #vectordb = Chroma.from_documents(split_docs, embedding=embedder, persist_directory=persist_dir)
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedder,
        client_settings=get_shared_settings(persist_dir)
    )
    vectordb.add_documents(split_docs)
    vectordb.persist()
    return vectordb.as_retriever()
