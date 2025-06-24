import os
from git import Repo
from repo_insight.embedder import load_embedder
from repo_insight.retriever import setup_retriever
from repo_insight.generator import build_qa_chain
from ingest import ingest_all
from repo_insight.utils.repo_manager import clone_or_pull_repo_from_url
import glob

REPO_ROOT = "repos"

def is_chroma_initialized(persist_dir: str) -> bool:
    return bool(glob.glob(os.path.join(persist_dir, "*.parquet")))  # Chroma v0.4形式ファイル確認

def answer_query(repo_url: str, query: str, pull: bool = False) -> str:
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = clone_or_pull_repo_from_url(repo_url, pull=pull)

    persist_dir = os.path.join("./chroma_db", repo_name)
    embedder = load_embedder()
    if not is_chroma_initialized(persist_dir):
        ingest_all(local_path, persist_dir, embedder)

    retriever = setup_retriever(persist_dir, embedder, local_path=local_path, reset=True)
    qa_chain = build_qa_chain(retriever)

    return qa_chain.invoke(query)
