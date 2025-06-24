import os
from git import Repo
from repo_insight.embedder import load_embedder
from repo_insight.retriever import setup_retriever
from repo_insight.generator import build_qa_chain
from ingest import ingest_all

REPO_ROOT = "repos"

def clone_or_pull_repo(repo_url: str, repo_name: str, pull: bool = False) -> str:
    local_path = os.path.join(REPO_ROOT, repo_name)
    if os.path.exists(local_path):
        if pull:
            print(f"🔄 Pulling latest changes in {local_path}...")
            repo = Repo(local_path)
            repo.remotes.origin.pull()
    else:
        print(f"⬇️ Cloning {repo_url} into {local_path}...")
        Repo.clone_from(repo_url, local_path)
    return local_path

def answer_query(repo_url: str, query: str, pull: bool = False) -> str:
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = clone_or_pull_repo(repo_url, repo_name, pull=pull)

    persist_dir = os.path.join("./chroma_db", repo_name)
    embedder = load_embedder()
    if not os.path.exists(persist_dir):
        ingest_all(local_path, persist_dir, embedder)

    retriever = setup_retriever(persist_dir, embedder, local_path=local_path, reset=False)
    qa_chain = build_qa_chain(retriever)

    return qa_chain.run(query)
